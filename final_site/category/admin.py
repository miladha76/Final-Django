from django.contrib import admin
from .models import Categories

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('cat_name',)}
    list_display=('cat_name','slug')

admin.site.register(Categories,CategoryAdmin)
