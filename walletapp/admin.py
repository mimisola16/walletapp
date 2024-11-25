from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.site_header = 'MIMI STORE'
admin.site.site_title = 'MIMI STORE Admin'

class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the admin interface
    list_display = ('email', 'user_name', 'name', 'gender', 'user_type', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'gender', 'user_type')
    search_fields = ('email', 'user_name', 'name')
    ordering = ('email',)

    # Define fieldsets for adding and changing user details
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_name', 'name', 'gender', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('User Type', {'fields': ('user_type',)}),
    )

    # Fields for creating a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Shop)
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Location)