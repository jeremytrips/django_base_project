from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Settings

# from users.api.serializers.RegistrationSerializer import RegistrationSerializer as R
# ser = R(data={"email": "Tedfdst@gmail.Com", "password": "12345de"})


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ('settings', 'id', 'last_login', 'is_superuser', 'groups', 'user_permissions')

    def save(self, **kwargs):
        kwargs["settings"] = Settings.objects.create()
        return super(RegistrationSerializer, self).save(**kwargs)
