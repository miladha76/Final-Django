from django.shortcuts import render,redirect
from .forms import RegistrationForm , UserForm , UserProfileForm
from .models import Account,UserProfile
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
from django.shortcuts import get_object_or_404
import redis
import random
from .utils import send_opt
from django import views
from .forms import Otploginform
from orders.models import Order,OrderItem
import requests




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
            r = redis.Redis(host='localhost', port=6379, db=0)
            otpcode = random.randint(100000, 999999)
            r.setex(email, 40, str(otpcode)) 
            request.session['email'] = email
            send_opt(str(otpcode))
            return redirect('otp_login')           
            messages.success(request, 'شما وارد شدید')
    
            


   

            
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
            messages.error(request, 'ورود خطا داشت')
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
        return redirect('dashboard')
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
    orders = Order.objects.order_by('-created_at').filter(user_id =request.user.id , is_ordered =True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id =request.user.id)
    
    context ={
        'orders_count':orders_count,
        'userprofile':userprofile,
    }
    return render(request, 'accounts/dashboard.html',context)



class Otplogin(views.View):
    def get(self, request):
        form = Otploginform()
        return render(request, 'accounts/otp_login.html', {'form': form})

    def post(self, request):
        form = Otploginform(request.POST)
        if form.is_valid():
            r = redis.Redis(host='localhost', port=6379, db=0)
            otp = request.session.get('username')
            print(otp)
            storedotp = r.get(otp).decode()
            if form.cleaned_data['code'] == storedotp:
                return redirect('dashboard')

        return redirect('otp_login')


def my_orders(request):
    orders = Order.objects.filter(user=request.user , is_ordered=True).order_by("-created_at")
    context ={
        'orders':orders,
        
    }
    return render(request,'accounts/my_orders.html',context)

def edit_profile(request):
    userprofile =get_object_or_404(UserProfile ,user =request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST , instance=request.user)
        profile_form = UserProfileForm(request.POST ,request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'پروفایل شما بروزرسانی شد')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
        }
    return render(request , 'accounts/edit_profile.html',context)

@login_required(login_url='login')
def order_detail(request,order_id):
    order_detail = OrderItem.objects.filter(order__order_number = order_id)
    order= Order.objects.get(order_number = order_id)
    subtotal=0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
        
    context = {
        "order_detail": order_detail,
        'order':order ,
        'subtotal': subtotal,
        
    }
    return render(request,'accounts/order_detail.html')
