from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_206_PARTIAL_CONTENT
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from users.permissions import IsEmailVerfied, IsAccountVisible

class DeleteAccount(APIView):
    """
        Manage the user deletion.
    """

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data=["DELETED"], status=HTTP_200_OK)