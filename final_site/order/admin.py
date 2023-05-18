from django.contrib import admin
from .models import PaymentDetails, OrderDetails, OrderItem

admin.site.register(PaymentDetails)
admin.site.register(OrderDetails)
admin.site.register(OrderItem)