from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import datetime
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import Settings

# from users.api.serializers.RegistrationSerializer import RegistrationSerializer as R
# ser = R(data={"email": "Tedfdst@gmail.Com", "password": "12345de"})

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'noma', 'student_card', 'studies', 'home_address', 'birth_date', 'description', 'profile_pic_one', 'profile_pic_two', 'profile_pic_three',  'first_name', 'last_name', 'password', 'password2']

    def create(self, validated_data):
        """
        Function used to create user. By default it does not implement password matching and password checking.
        """
        if validated_data["password"] != validated_data["password2"]:
            raise serializers.ValidationError("PASSWORD_DO_NOT_MATCH")
        try:
            validate_password(validated_data["password"])
        except ValidationError as e:
            raise serializers.ValidationError(e)
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
