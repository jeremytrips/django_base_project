from rest_framework import serializers


class ValidationTokenSerializer(serializers.Serializer):
    user_email = serializers.EmailField(required=True)
    token =serializers.CharField(required=True)
