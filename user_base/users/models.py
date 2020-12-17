from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from inclusive_django_range_fields import InclusiveIntegerRangeField
from users.managers import CustomUserManager

class Settings(models.Model):

    is_email_verified = models.BooleanField(default=False)
    account_is_visible = models.BooleanField(default = True)

    push_notification_new_relation = models.BooleanField(default=True)
    mail_notification_new_relation = models.BooleanField(default=True)
    push_notification_new_message = models.BooleanField(default=True)
    mail_notification_new_message = models.BooleanField(default=True)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)                                                  # Adresse mail pour contacter et se connecter
    noma = models.CharField(max_length=10)                                                  # Numero de matricule de l etudiant(e)
    student_card = models.ImageField(upload_to="image/student_card/")                       # Carte etudiant pour verif mail/noma/nom et validite du compte
    first_name = models.CharField(max_length=20,)                                           # prenom de l etudiant(e)
    last_name = models.CharField(max_length=20,)                                            # nom de l etudiant(e)
    studies = models.CharField(max_length=30,)                                              # etudes de l etudiant(e)
    home_address = models.CharField(max_length=30,)                                         # lieu de residence hors campus
    birth_date = models.DateTimeField(auto_now=True, blank=True)                            # date de naissance de l etudiant(e)
    description = models.CharField(max_length=250, blank=True)                              # description visible pour les autres utilisateurs
    age_lower_bound = models.PositiveSmallIntegerField(default=16)                          # limite inf d age pour partenaire
    age_upper_bound = models.PositiveSmallIntegerField(default=100)                         # limite sup d age pour partenaire
    profile_pic_one = models.ImageField(blank=True, default = "/static/no_img.png", upload_to="image/profile/")            # premiere image de l'utilisateur
    profile_pic_two = models.ImageField(blank=True, upload_to="image/profile/")                                         # deuxieme image de l'utilisateur
    profile_pic_three = models.ImageField(blank=True, upload_to="image/profile/")                                       # troisieme image de l'utilisateur
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
