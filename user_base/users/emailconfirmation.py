from django.core.mail import send_mail
from django.conf import settings
from users.models import EmailVerificationToken
from django.contrib.auth import get_user_model

from threading import Thread


def send_confirmation_email(user, token):
    t = Thread(target=_send_confirmation_email, args=(user, token.token))
    t.start()

def _send_confirmation_email(user, token):
    send_mail(
        subject=settings.VERIFICATION_EMAIL_SUBJECT,
        message=settings.VERIFICATION_EMAIL_CONTENT.format(first_name=user.first_name, token=token),
        from_email=None, 
        recipient_list=[user.email,],
        fail_silently=False
    )

def verify_email(user_mail, furnished_token):
    user = get_user_model().objects.get(email=user_mail)
    user_token = EmailVerificationToken.objects.get(user_owner=user)
    if user_token.token == furnished_token:
        user_token.delete()
        return user, True
    else: 
        return None, False 