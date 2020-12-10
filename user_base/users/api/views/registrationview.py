from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_206_PARTIAL_CONTENT
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from users.api.serializers.RegistrationSerializer import RegistrationSerializer
from users.models import EmailVerificationToken
from users.emailconfirmation import send_confirmation_email
import random

def generate_random_numer(num):
    a = ""
    for i in range(num):
        a+= str(random.randint(0, 9))
    return a


class RegistrationView(APIView):
    """
    Manage user registration
    """
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_verification_token = generate_random_numer(6)
            token_object = EmailVerificationToken.objects.create(user_owner=user, token=user_verification_token)
            send_confirmation_email(user, token_object)
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=HTTP_206_PARTIAL_CONTENT)
