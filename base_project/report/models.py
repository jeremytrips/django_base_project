from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class ReportUser(models.Model):
    user_reporting = models.EmailField()
    user_reported = models.EmailField()
    reasons_choices = [                                             # L utilisateur doit choisir parmis ces choix une raison de signalement
        (fake_profile, 'Faux profil'),
        (inappropriate_pic, 'Photo inappropriee'),
        (inappropriate_behavior, 'Comportement inapproprie'),
        (other, 'Autre'),
    ]
    reason = models.CharField(
        max_length = 250,
        choices=reasons_choices,
    )
    user_report_description = models.CharField(max_length = 250)
    #chat_log = 