from django.urls import path
from . import views
from .api_views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'UserProfileViewSet',UserProfileViewSet,basename='UserProfileViewSet')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('otp_login/', views.otplogin, name='otp_login'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/',views.edit_profile,name = 'edit_profile'),
    path('change_password/',views.change_password,name = 'change_password'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    path('api/edit_profile/',UserProfileEditAPIView.as_view(),name='edit_profilee'),
    path('api/dashboardd/',dashboardd,name='dashboardd'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
   
]
