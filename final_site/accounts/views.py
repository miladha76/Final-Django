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
import requests

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

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

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

            
            auth.login(request, user)
            messages.success(request, 'شما وارد شدید')
            otp_code = generate_otp()  # Replace with your OTP code generation logic
            
            send_opt(otp_code)  # Call your send_otp method with the OTP code

            # Store the received OTP and user details in the session for OTP verification
            request.session['received_otp'] = otp_code
            request.session['user_id'] = user.id

            return redirect('otp_login')
            # url = request.META.get('HTTP_REFERER')
            # try:
            #     query = requests.utils.urlparse(url).query
            #     # next=/cart/checkout/
            #     params = dict(x.split('=') for x in query.split('&'))
            #     if 'next' in params:
            #         nextPage = params['next']
            #         return redirect(nextPage)                
            # except:
            #     return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

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



def otp_login(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        received_otp = request.session.get('received_otp')
        user_id = request.session.get('user_id')

        if otp == received_otp:
            user = Account.objects.get(id=user_id)  # Retrieve the user based on user_id
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('otp_login')
    return render(request, 'accounts/otp_login.html')
