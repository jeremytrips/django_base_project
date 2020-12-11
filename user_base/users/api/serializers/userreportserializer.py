from rest_framework import serializers

class UserReportSerializer(serializers.Serializer):
    """
    Serializer to report user.
    reported_user must contain an int that is the pk of the reported user.
    """
    reason = serializers.CharField(max_length=250, required=True)
    reported_user = serializers.IntegerField(required=True)
