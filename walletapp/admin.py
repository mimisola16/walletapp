from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.site_header = 'MIMI STORE'
admin.site.site_title = 'MIMI STORE Admin'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('user_name', 'name', 'gender', 'email','user_type', 'is_active', 'is_staff')
    search_fields = ('name', 'email')
    list_filter = ('is_active', 'is_staff', 'gender','user_type')
    ordering = ('user_name','name')
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Shop)
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Location)