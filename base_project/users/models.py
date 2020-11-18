from django.contrib.auth.models import AbstractUser
from django.db import models
from inclusive_django_range_fields import InclusiveIntegerRangeField
# Create your models here.

class CustomUser(AbstractUser):
    
    user_name = None                                            #Pas de nom d'utilisateur, on utilise adresse mail pour se connecter
    mail = models.EmailField()                                  #Adresse mail pour contacter et se connecter
    noma = models.CharField(max_length = 10)                    #Numero de matricule de l etudiant(e)
    student_card = models.ImageField()                          #Carte etudiant pour verif mail/noma/nom et validite du compte
    first_name = models.CharField(max_length = 20)                    #prenom de l etudiant(e)
    last_name = models.CharField(max_length = 20)                 #nom de l etudiant(e)
    studies = models.CharField(max_length = 30)                 #etudes de l etudiant(e)
    hometown = models.CharField(max_length = 30)             #lieu de residence hors campus
    birth_date = models.DateTimeField()                          #date de naissance de l etudiant(e)
    description = models.CharField(max_length = 250)            #description visible pour les autres utilisateurs
    account_is_visible = models.BooleanField()                  #le compte est visible ou inactif
    interest_age_fork = InclusiveIntegerRangeField()            #fourchette d age d interet pour partenaire
    profile_pic_one = models.ImageField(blank=True)                         #image de l'utilisateur
    profile_pic_two = models.ImageField(blank=True)                         #image de l'utilisateur
    profile_pic_three = models.ImageField(blank=True)                       #image de l'utilisateur
    email_verified = models.BooleanField(default = False)                   #adresse email validee via mail
    settings = models.OneToOneField(Settings, on_delete = models.CASCADE)

    def __str__(self):
        return self.username


class Settings(Models.model):

    push_notification_new_relation = models.BooleanField()                  # s explique de par le nom
    mail_notification_new_relation = models.BooleanField()
    push_notification_new_message = models.BooleanField()
    mail_notification_new_message = models.BooleanField()