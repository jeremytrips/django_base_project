from django.contrib import admin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser, Settings, EmailVerificationToken


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(EmailVerificationToken)
admin.site.register(CustomUser)
admin.site.register(Settings)
