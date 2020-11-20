from django.core.exceptions import PermissionDenied
from django.utils import inspect
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import exceptions

from django.contrib.auth import get_user_model, authenticate

# Todo add messaging device and device type on serializer when using firebase for backend notifications


class LoginSerializer(ModelSerializer):
    """

        LoginSerializer
        ===============
            Custom login serializer.
    """
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', )

    def validate(self, data):
        user = authenticate(**data)
        try:
            data['user'] = user
            return data
        except exceptions.AuthenticationFailed as e:
            return False
