from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from inclusive_django_range_fields import InclusiveIntegerRangeField
from .managers import CustomUserManager
from .other_models.settings import Settings


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)                                                  # Adresse mail pour contacter et se connecter
    noma = models.CharField(max_length=10, default = "NoNoma")                              # Numero de matricule de l etudiant(e)
    student_card = models.ImageField(default = "\static\no_img.png")                        # Carte etudiant pour verif mail/noma/nom et validite du compte
    name = models.CharField(max_length=20, default = "NoName")                              # prenom de l etudiant(e)
    surname = models.CharField(max_length=20, default="NoSurname")                          # nom de l etudiant(e)
    studies = models.CharField(max_length = 30, default = "NoStudies")                      # etudes de l etudiant(e)
    home_adress = models.CharField(max_length=30, default = "NoHomeAdd")                    # lieu de residence hors campus
    birth_date = models.DateTimeField(auto_now=True, auto_created=True)                                  # date de naissance de l etudiant(e)
    description = models.CharField(max_length=250, default="")                              # description visible pour les autres utilisateurs
    age_lower_bound = models.PositiveSmallIntegerField(default=16)                          # limite inf d age pour partenaire
    age_upper_bound = models.PositiveSmallIntegerField(default=100)                         # limite sup d age pour partenaire
    profile_pic_one = models.ImageField(blank=True, default = "\static\no_img.png")            # premiere image de l'utilisateur
    profile_pic_two = models.ImageField(blank=True, default = "\static\no_img.png")            # deuxieme image de l'utilisateur
    profile_pic_three = models.ImageField(blank=True, default = "\static\no_img.png")          # troisieme image de l'utilisateur
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
