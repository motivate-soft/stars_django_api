from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser


#
#
admin.site.register(CustomUser, CustomUserAdmin)
