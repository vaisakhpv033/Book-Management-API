from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
        "is_blocked",
    )
    ordering = ("-date_joined",)



admin.site.register(User, CustomUserAdmin)

