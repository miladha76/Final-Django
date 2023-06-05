from django.urls import path,include
from . import views
from .api_views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'OrderViewSet',OrderViewSet,basename='Orderviewset')


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/',views.order_complete,name= 'order_complete'),
    path('api/order/', include(router.urls)),
    path('api/payments/',payments,name='payments'),
    path('api/place_order/',place_order,name='place_order'),
    path('api/order_complete/',payments,name='order_complete'),
    
]   

