from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from .other_models.settings import Settings


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        s = Settings()
        s.is_admin = True
        s.is_staff = True
        s.email_verified = True
        s.save()
        extra_fields["settings"] = s
        return self.create_user(email, password, **extra_fields)
