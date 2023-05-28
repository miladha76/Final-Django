from django.urls import path
from . import views
from .views import Otplogin

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('otp_login/', Otplogin.as_view(), name='otp_login'),
    path('my_orders/',views.my_orders,name='my_orders'),
   
]
