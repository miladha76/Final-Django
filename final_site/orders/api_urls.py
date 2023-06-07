from django.urls import path
from .views import PaymentAPIView, OrderAPIView, OrderItemAPIView

urlpatterns = [
    path('payments/', PaymentAPIView.as_view(), name='paymentss'),
    path('order-items/', OrderItemAPIView.as_view(), name='order-items'),
    path('orders/<int:pk>/', OrderAPIView.as_view(), name='order-detail'),
]
