from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from inclusive_django_range_fields import InclusiveIntegerRangeField
from .managers import CustomUserManager
from .other_models.settings import Settings


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)                                  # Adresse mail pour contacter et se connecter
    noma = models.CharField(max_length=10)                                  # Numero de matricule de l etudiant(e)
    student_card = models.ImageField()                                      # Carte etudiant pour verif mail/noma/nom et validite du compte
    name = models.CharField(max_length=20)                                  # prenom de l etudiant(e)
    surname = models.CharField(max_length=20)                               # nom de l etudiant(e)
    studies = models.CharField(max_length = 30)                             # etudes de l etudiant(e)
    home_adress = models.CharField(max_length=30)                         # lieu de residence hors campus
    birt_date = models.DateTimeField()                                      # date de naissance de l etudiant(e)
    description = models.CharField(max_length=250)                        # description visible pour les autres utilisateurs
    account_is_visible = models.BooleanField()                              # le compte est visible ou inactif
    interest_age_fork = InclusiveIntegerRangeField()                        # fourchette d age d interet pour partenaire
    profile_pic_one = models.ImageField(blank=True)                         # image de l'utilisateur
    profile_pic_two = models.ImageField(blank=True)                         # image de l'utilisateur
    profile_pic_three = models.ImageField(blank=True)                       # image de l'utilisateur
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
