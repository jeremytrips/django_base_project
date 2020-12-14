from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_206_PARTIAL_CONTENT, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from users.api.serializers.LoginSerializer import LoginSerializer
from users.models import EmailVerificationToken


class LoginVIew(ObtainAuthToken):
    """
    View used to create user auth token.
    """
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        """
        Handle the login request by verifying the user status.
        """
        serializer = LoginSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user is None:
                # Credentials errors
                return Response(data=["REGISTER_FIRST"], status=HTTP_401_UNAUTHORIZED)
            if not user.settings.is_email_verified:
                # User emil must be verified before he can connect
                return Response(["VERIFY_EMAIL_FIRST"], HTTP_401_UNAUTHORIZED)
            token, created = Token.objects.get_or_create(user=user)
            if user.is_active:
                # User can connect the API
                # todo get user list and pass it in the response
                return Response({
                    "token": token.key
                }, HTTP_200_OK)
            else:
                # User has disable his account
                return Response(["USER_INACTIVE"], HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, HTTP_206_PARTIAL_CONTENT)


class LogoutView(APIView):
    """
    View that handle logout request
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        Handle the get request by deleting the user token. He can't access api until he create a new one.
        """
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)
