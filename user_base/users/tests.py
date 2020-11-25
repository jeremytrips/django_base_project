import django
import os
import copy

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files import File

import rest_framework.status as status
from rest_framework.exceptions import ErrorDetail
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token


from users.models import Settings
from users.api.serializers.RegistrationSerializer import RegistrationSerializer
from users.api.serializers.LoginSerializer import LoginSerializer
from users.api.views.authentication import LoginVIew
from test_data import serializer_create_correct_data, serializer_create_different_password_data


# todo
"""
Things already tested:
    - User model:
        - create user
        - create superuser
    - Registration view:
        - Correct data
        - Duplicated email 
        - missing data
    - Login View:
        - not_email_verified
        - unregistered client
        - correct login
    - RegistrationSerializer
        - correct data
        - different password
        - weak password
"""

User = get_user_model()


class UserAuthenticationView(TestCase):

    def setUp(self):
        user = User.objects.create(email='login@user.com', password='fezruighfrjeg5', settings=Settings.objects.create())
        user.settings.is_email_verified = True
        user.save()

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
            raise Exception("Data 'serializer_create_correct_data' should be correct at this point and serializer should be valid.")

        
    def test_different_password_serializer(self):
        """
        Test different password in serializer
        """
        ser = RegistrationSerializer(data=serializer_create_different_password_data)
        if ser.is_valid():
            self.assertRaises(serializers.ValidationError, ser.save)
    
    def test_weak_password_serializer(self):
        """
        Test weak password in serializer
        """
        ser = RegistrationSerializer(data=serializer_create_different_password_data)
        if ser.is_valid():
            self.assertRaises(serializers.ValidationError, ser.save)

    def test_register_view(self):
        """
        Test the basic registrations workflow
        """
        data = {
            "email": "jeremy.trips@tamere.com",
            "password": "pdcdezgf4545freff",
            "password2": "pdcdezgf4545freff",
            "home_address": "Zaventem",
            "studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        resp = self.client.post(reverse("create"), data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data, None)

    def test_second_user(self):
        """
        Test the basics registration workflow plus another user trying to registrate with same credentials.
        """
        self.test_register_view()
        data = {
            "email": "jeremy.trips@tamere.com",
            "password": "pdcdezgf4545freff",
            "password2": "pdcdezgf4545freff",
            "home_address": "Zaventem",
            "studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        data_second_user = data
        resp = self.client.post(reverse("create"), data=data_second_user)
        self.assertEqual(resp.data["email"][0], "custom user with this email already exists.")    
        self.assertEqual(resp.data["email"][0].code, "unique")
        self.assertEqual(resp.status_code, 206)

    def test_not_correct_data_registration_view(self):
        """
        Test the errors throw if data are missing in the serializer.
        """
        data = {
            "email": "jeremy.trips@tamere.com",
            "password": "pdcdezgf4545freff",
            "password2": "pdcdezgf4545freff",
            "home_address": "Zaventem",
            #"studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        resp = self.client.post(reverse("create"), data=data)
        self.assertEqual(resp.status_code, 206)
        self.assertIn("studies", resp.data.keys())

    def test_not_email_verified_login_view(self):
        """
        Test user want to connect without having verified his email.
        """
        data = {
            "email": "jeremy.trips@tamere.com",
            "password": "pdcdezgf4545freff",
            "password2": "pdcdezgf4545freff",
            "home_address": "Zaventem",
            "studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        self.client.post(reverse("create"), data=data)
        resp = self.client.post(reverse("login"), data={"email": "jeremy.trips@tamere.com", "password": 'pdcdezgf4545freff'})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(resp.data, "NOT_EMAIL_VERIFIED")
    
    def test_login_view(self):
        """
        Test basic login workflow
        """
        data = {
            "email": "jeremy.trips@tamere.com",
            "password": "pdcdezgf4545freff",
            "password2": "pdcdezgf4545freff",
            "home_address": "Zaventem",
            "studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        self.client.post(reverse("create"), data=data)
        user = User.objects.get(email="jeremy.trips@tamere.com")
        user.settings.is_email_verified = True
        user.settings.save()
        user.save()
        resp = self.client.post(reverse("login"), data={"email": "jeremy.trips@tamere.com", "password": 'pdcdezgf4545freff'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['token']), 40)
        self.assertEqual(resp.data['token'], Token.objects.get(user=user).key)
    
    def test_login_unknown_view(self):
        """
        Test basic workflow with unknown credential
        """
        resp = self.client.post(reverse("login"), data={"email": "none@tamere.com", "password": 'pdcdezgf4545freff'})
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.data, "USER_DO_NOT_EXIST")
 
    def test_create_user(self):
        """
        Test create a user
        """
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
        """
        Test create a super user
        """
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
