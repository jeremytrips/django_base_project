from django.db import models


class Settings(models.Model):

    email_verified = models.BooleanField(default=False)
    account_is_visible = models.BooleanField(default = True)                             

    push_notification_new_relation = models.BooleanField(default=True)               
    mail_notification_new_relation = models.BooleanField(default=True)
    push_notification_new_message = models.BooleanField(default=True)
    mail_notification_new_message = models.BooleanField(default=True)

