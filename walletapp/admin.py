from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Shop)
admin.site.register(Categories)
admin.site.register(Product)