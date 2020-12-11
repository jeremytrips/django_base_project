from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from users.api.serializers.userreportserializer import UserReportSerializer
from users.models import ReportedUser
from users.permissions import IsActive, IsEmailVerfied

User = get_user_model()

class ReportUser(APIView):
    """
    View used to report a user.
    """
    permission_classes = [IsAuthenticated, IsActive, IsEmailVerfied]
    def post(self, request):
        ser = UserReportSerializer(data=request.data)
        if ser.is_valid():
            try:
                user_reported = User.objects.get(pk=ser.validated_data["reported_user"])
            except User.DoesNotExist:
                return Response(data=["REPORTED_USER_DOES_NOT_EXIST"], status=HTTP_400_BAD_REQUEST)
            if not user_reported.settings.is_email_verified:
                return Response(data=["REPORTED_USER_NOT_EMAIL_VERIFIED"], status=HTTP_400_BAD_REQUEST)
              if user_reported == request.user:
                return Response(data=["SELF_REPORT_NOT_ALLOWED"], status=HTTP_400_BAD_REQUEST)
            report = ReportedUser.objects.create(
                user_report_description=ser.validated_data["reason"]
            )
            report.user_reported.add(user_reported)
            report.user_reporting.add(request.user)
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)