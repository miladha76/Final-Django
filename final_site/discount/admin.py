from django.contrib import admin
from .models import Discount


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percent', 'created_at', 'modified_at')
    list_filter = ('created_at', 'modified_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    
admin.site.register(Discount,DiscountAdmin)
