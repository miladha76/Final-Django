from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress, UserPayment


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_superuser','last_login','date_joined')
    list_display_links=('username','first_name', 'last_name')
    readonly_fields=('last_login','date_joined')
    ordering=('-date_joined',)
    
    filter_horizontal=()
    list_filter=()
    fieldsets=() 


# Register the models with the respective admins
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAddress)
admin.site.register(UserPayment)
