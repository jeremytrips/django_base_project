from django.contrib import admin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser, Settings


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser)
admin.site.register(Settings)
