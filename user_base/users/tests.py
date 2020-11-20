from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import django
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ErrorDetail
from rest_framework import serializers
from users.models import Settings
from users.api.serializers.RegistrationSerializer import RegistrationSerializer
from test_data import serializer_create_correct_data, serializer_create_different_password_data


# todo
"""
    LOGIN: with different user status
    LOGOUT: and check for token deleted
"""

User = get_user_model()
client = Client()


class UserAuthenticationView(TestCase):

    def setUp(self):
        # self.user = User.objects.create(**create_correct_data)
        pass

    def test_correct_register_serializer(self):
        """
        Test the creation of a user using it's .
        """        
        ser = RegistrationSerializer(data=serializer_create_correct_data)
        self.assertTrue(ser.is_valid(), "Serializer error")
        self.assertDictEqual(ser.errors, {}, "Errors in correct data serializer")
        if ser.is_valid():
            user = ser.save()
            user2 = User.objects.last()
            self.assertEqual(user, user2)
        else:
            raise Exception("Data 'serializer_create_correct_data' should be correct at this point ans serializer should be valid.")

        
    def test_different_password_serializer(self):
        """
        Test different password in serializer
        """
        ser = RegistrationSerializer(data=serializer_create_different_password_data)
        if ser.is_valid():
            self.assertRaises(serializers.ValidationError, ser.save)
    
    def test_weak_password_serializer(self):
        """
        Test different password in serializer
        """
        ser = RegistrationSerializer(data=serializer_create_different_password_data)
        if ser.is_valid():
            self.assertRaises(serializers.ValidationError, ser.save)

    def test_create_user(self):
        User = get_user_model()
        settings = Settings.objects.create()
        user = User.objects.create_user(email='normal@user.com', password='foo', settings=settings)
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)

        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        settings = Settings.objects.create()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(django.db.utils.IntegrityError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', settings=settings)
