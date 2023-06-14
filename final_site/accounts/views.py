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
from django.core.mail import send_mail




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


def send_otp_email(email, otp_code):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = 'django.milad@gmail.com'  # Replace with your email address

    send_email=EmailMessage(subject, message, from_email,to=[email])
    send_email.send()
    
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
            otp_code = random.randint(100000, 999999)
            r.setex(email, 40, str(otp_code)) 
            request.session['email'] = email
            send_otp_email(email, otp_code)
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





def otplogin(request):
    if request.method == 'POST':
        form = Otploginform(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['code']
            email = request.session.get('email')

            # Retrieve the OTP code from Redis
            r = redis.Redis(host='localhost', port=6379, db=0)
            saved_otp_code = r.get(email)

            if saved_otp_code is not None and otp_code == saved_otp_code.decode():
                # OTP code matches
                user = Account.objects.get(email=email)
                auth.login(request, user)
                r.delete(email)  # Delete the OTP code from Redis
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid OTP code')
                auth.logout(request)  # Logout the user
                return redirect('login')
    else:
        form = Otploginform()

    return render(request, 'accounts/otp_login.html', {'form': form})

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user , is_ordered=True).order_by("-created_at")
    context ={
        'orders':orders,
        
    }
    return render(request,'accounts/my_orders.html',context)


@login_required(login_url='login')
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
    return render(request,'accounts/order_detail.html',context)
@login_required(login_url='login')
def change_password(request):
    if request.method=='POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user=Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'رمز با موفقیت تغییر کرد')
                return redirect('change_password')
            else:
                messages.error(request,'رمز درست را وارد کنید')
                return redirect('change_password')
        else:
            messages.error(request,'رمز مشابه نیست')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'بازیابی رمز'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'ایمیل تنظیم مجدد رمز عبور به آدرس ایمیل شما ارسال شده است.')
            return redirect('login')
        else:
            messages.error(request, 'حساب شما وجود ندارد')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'لطفاً رمز عبور خود را بازیابی کنید')
        return redirect('resetPassword')
    else:
        messages.error(request, 'این لینک منقضی شده است!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'رمز با موفقیت تغییر کرد')
            return redirect('login')
        else:
            messages.error(request, 'رمز ها مشابه نیست')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')