from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from users.emailconfirmation import verify_email
from users.api.serializers.validationtokenserializer import ValidationTokenSerializer
from users.permissions import IsActive, IsAccountVisible
from rest_framework.permissions import AllowAny

class VerifyToken(APIView):
    """
    View used to match token recieved by the user and the stored one.
    """
    permission_classes = [AllowAny,]

    def post(self, request):
        ser = ValidationTokenSerializer(data=request.data)
        if ser.is_valid():
            user, res = verify_email(ser.validated_data['user_email'], ser.validated_data['token'])
            if res:
                user.settings.is_email_verified = True
                user.save()
                return Response(status=HTTP_200_OK)
            else:
                return Response(data=["TOKEN_ERROR"], status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data=ser.errors, status=HTTP_400_BAD_REQUEST)