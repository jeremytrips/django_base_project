from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_206_PARTIAL_CONTENT
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from users.api.serializers.RegistrationSerializer import RegistrationSerializer


class RegistrationView(APIView):
    """
    Manage user registration
    """
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=HTTP_206_PARTIAL_CONTENT)
