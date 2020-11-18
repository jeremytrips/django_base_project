from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ('settings', 'id', 'last_login', 'is_superuser', 'groups', 'user_permissions')
