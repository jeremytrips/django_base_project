from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from inclusive_django_range_fields import InclusiveIntegerRangeField
from users.managers import CustomUserManager

class Settings(models.Model):

    is_email_verified = models.BooleanField(default=False)

    allow_push_notification = models.BooleanField(default=True)
    allow_email_notification = models.BooleanField(default=True)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20,)
    last_name = models.CharField(max_length=20,)
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_user_report(self):
        print(rmodels.ReportedUser.objects.get(user_reported=self))
        # todo

    def save(self, *args, **kwargs):
        return super(CustomUser, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.email


class EmailVerificationToken(models.Model):
    """
    Token a created when user register to the site. The token is then send to 
    the user for him to verify his email address
    """
    user_owner = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE)
    token = models.CharField(max_length=6)

class ReportedUser(models.Model):
    """
    Model that will store reported user.

    """
    user_reporting = models.ManyToManyField(to=CustomUser, related_name="user_reporting")
    user_reported = models.ManyToManyField(to=CustomUser, related_name="user_reported")
    user_report_description = models.CharField(max_length = 250)
