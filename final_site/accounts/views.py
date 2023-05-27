from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.models import Cart,CartItem
from carts.views import _cart_id
import redis
import random
from .utils import send_opt
from django import views

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def generate_otp():
    """Generate a random 6-digit OTP code."""
    return str(random.randint(100000, 999999))


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
           

                       
            current_site = get_current_site(request)
            mail_subject = 'لطفاً حساب کاربری خود را فعال کنید'
            message = render_to_string('accounts/account_email_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password) 
        if user is not None:
            otp_code = request.POST.get('otp_code')
            if otp_code:
                # Check if OTP code is valid
                saved_otp = redis_client.get(user.username)
                if saved_otp and otp_code == saved_otp.decode():
                    # Delete OTP code from Redis after successful verification
                    redis_client.delete(user.username)
                else:
                    messages.error(request, 'Invalid OTP code')
                    return redirect('login')
            else:
                # Generate OTP code and store it in Redis
                otp_code = generate_otp()
                redis_client.setex(user.username, 300, otp_code)
                send_opt(str(otp_code))
                return render(request, 'accounts/otp_login.html')       
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                   

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request, 'شما وارد شدید')
            return redirect('dashboard')
        else:
            messages.error(request, 'ورود انجام نشد')
            return redirect('login')  
        
    return render(request,'accounts/login.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'تبریک می‌گوییم! حساب کاربری شما فعال شده است.')
        return redirect('login')
    else:
        messages.error(request, 'لینک فعال‌سازی نامعتبر است')
        return redirect('register')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'شما خارج شدید.')
    return redirect('login')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


class OtploginView(views.View):
    def get(self, request):
        form = Otploginform()
        return render(request, 'otp_login.html', {'form': form})

    def post(self, request):
        form = Otploginform(request.POST)
        if form.is_valid():
            r = redis.Redis(host='localhost', port=6379, db=0)
            otp = request.session.get('username')
            print(otp)
            storedotp = r.get(otp).decode()
            if form.cleaned_data['code'] == storedotp:
                return redirect('/')

        return redirect('otp')