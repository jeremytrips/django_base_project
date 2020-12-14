from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from users.emailconfirmation import verify_email
from users.api.serializers.validationtokenserializer import ValidationTokenSerializer
from users.permissions import IsActive
from rest_framework.permissions import AllowAny

User = get_user_model()

class VerifyToken(APIView):
    """
    View used to match token recieved by the user and the stored one.
    """
    permission_classes = [AllowAny,]

    def post(self, request):
        ser = ValidationTokenSerializer(data=request.data)
        if ser.is_valid():
            try:
                user = User.objects.get(email=ser.validated_data['user_email'])
            except User.DoesNotExist:
                return Response(["DO_NOT_EXIST"], status=HTTP_400_BAD_REQUEST)
            user, res = verify_email(user, ser.validated_data['token'])
            if res: 
                user.settings.is_email_verified = True
                user.settings.save()
                return Response(status=HTTP_200_OK)
            else:
                return Response(data=["TOKEN_ERROR"], status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data=ser.errors, status=HTTP_400_BAD_REQUEST)