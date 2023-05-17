from django.contrib import admin
from order.models import Orderr, OrderItem,Payments



class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'payment','created_date', 'modified_date')
    list_filter = ('created_date', 'modified_date')
    search_fields = ('user__username', 'payment__payment_id')
    date_hierarchy = 'created_date'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'created_date', 'modified_date')
    list_filter = ('created_date', 'modified_date')
    search_fields = ('order__user__username', 'product__name')
    date_hierarchy = 'created_date'

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__user__username', 'order__id')
    date_hierarchy = 'created_at'
    



admin.site.register(Orderr,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Payments,PaymentsAdmin)