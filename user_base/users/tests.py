import django
import os
import copy

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files import File
import django.core.exceptions as exceptions

import rest_framework.status as status
from rest_framework.exceptions import ErrorDetail
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token


from users.models import Settings, EmailVerificationToken
from users.api.serializers.RegistrationSerializer import RegistrationSerializer
from users.api.serializers.LoginSerializer import LoginSerializer
from users.api.views.authentication import LoginVIew
from users.api.serializers.userreportserializer import UserReportSerializer
from test_data import serializer_create_correct_data, serializer_create_different_password_data, serializer_create_weak_password_data


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

class RegisterTest(TestCase):
    password = "czgv5fv4r51g1vr"

    def create_user(self, email):
        data = {
            "email": email,
            "password": self.password,
            "password2": self.password,
            "home_address": "Zaventem",
            "studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        return self.client.post(reverse("create"), data=data)

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
        self.create_user("test@me.com")
        resp = self.create_user("test@me.com")
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
            # "first_name": "jeremy",
            "last_name": "Trips"
        }
        resp = self.client.post(reverse("create"), data=data)
        self.assertEqual(resp.status_code, 206)
        self.assertIn("first_name", resp.data.keys())

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
        ser = RegistrationSerializer(data=serializer_create_weak_password_data)
        if ser.is_valid():
            self.assertRaises(serializers.ValidationError, ser.save)

class AuthenticationTest(TestCase):
    password = "dezuhfjrckpegftro"

    def create_user(self, email):
        data = {
            "email": email,
            "password": self.password,
            "password2": self.password,
            "home_address": "Zaventem",
            "studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        return self.client.post(reverse("create"), data=data)

    def test_not_email_verified_login_view(self):
        """
        Test user want to connect without having verified his email.
        """
        self.create_user("oui@encore.com")
        resp = self.client.post(reverse("login"), data={"email": "oui@encore.com", "password": self.password})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(resp.data, "VERIFY_EMAIL_FIRST")
    
    def test_login_view(self):
        """
        Test basic login workflow
        """
        email = "jaiplusaucune@inspi.com"
        self.create_user(email)
        user = User.objects.get(email=email)
        user.settings.is_email_verified = True
        user.settings.save()
        user.save()
        resp = self.client.post(reverse("login"), data={"email": email, "password": self.password})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['token']), 40)
        self.assertEqual(resp.data['token'], Token.objects.get(user=user).key)

    def test_login_unknown_view(self):
        """
        Test basic workflow with unknown credential
        """
        resp = self.client.post(reverse("login"), data={"email": "none@tamere.com", "password": 'pdcdezgf4545freff'})
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.data, "REGISTER_FIRST")
    
    def test_delete_user(self):
        email = "plusque@qqes.un"
        self.create_user(email)
        user = User.objects.get(email=email)
        email_token = EmailVerificationToken.objects.get(user_owner=user)
        self.client.post(reverse("verify_token"), data={
            "user_email": user.email,
            "token": email_token.token
        })
        resp = self.client.post(reverse("login"), data={
            "email": email,
            "password": self.password
        })
        token = resp.data["token"]
        resp = self.client.post(reverse("delete"), HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, ["DELETED"])
    


class UserAuthenticationView(TestCase):
    password = "dezuhfjrckpegftro"

    def setUp(self):
        user = User.objects.create(email='login@user.com', password='fezruighfrjeg5', settings=Settings.objects.create())
        user.settings.is_email_verified = True
        user.save()
 
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

class MailTest(TestCase):

    def create_user(self, email):
        data = {
            "email": email,
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
    
    def get_token(self, user):
        return EmailVerificationToken.objects.get(user_owner=user)
    
    def test_correct_token(self):
        """
        Test the correct email verification token
        """
        email = "jeremy.trips@gmail.com"
        self.create_user(email)
        user = User.objects.get(email=email)
        token = self.get_token(user)
        self.assertIsNotNone(token)
        resp = self.client.post(reverse("verify_token"), data={
            "user_email": email,
            "token": token.token
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.post(reverse("login"), data={"email": email, "password": 'pdcdezgf4545freff'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("token", resp.data.keys())
        self.assertRegexpMatches(resp.data["token"], r"[a-z0-9]{40}")

    def test_wrong_token(self):
        """
        Test the wrong email verification token
        """
        email = "test@me.com"
        self.create_user(email)
        user = User.objects.get(email=email)
        token = self.get_token(user)
        resp = self.client.post(reverse("verify_token"), data={
            "user_email": email,
            "token": "256"
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data, ["TOKEN_ERROR"])
    
    def test_not_register(self):
        """
        Test not register user trying ot verify email
        """
        email = "bonjour@oui.com"
        resp = self.client.post(reverse("verify_token"), data={
            "user_email": email,
            "token": "256"
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data, "DO_NOT_EXIST")

    def test_already_verified(self):
        """
        Test already verified user trying to verify his email
        """
        email = "girafe@gogole.com"
        self.create_user(email)
        user = User.objects.get(email=email)
        token = self.get_token(user)
        self.client.post(reverse("verify_token"), data={
            "user_email": email,
            "token": token.token
        })
        with self.assertRaises(EmailVerificationToken.DoesNotExist):
            EmailVerificationToken.objects.get(user_owner=user)
        resp = self.client.post(reverse("verify_token"), data={
            "user_email": email,
            "token": token.token
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data, ["TOKEN_ERROR"])
        resp = self.client.post(reverse("login"), data={"email": email, "password": 'pdcdezgf4545freff'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("token", resp.data.keys())
        self.assertRegexpMatches(resp.data["token"], r"[a-z0-9]{40}")

class UserReportTest(TestCase):
    password = "pdcdezgf4545freff"
    
    def createUser(self, email):
        data = {
            "email": email,
            "password": self.password,
            "password2": self.password,
            "home_address": "Zaventem",
            "studies": "Ingé de ouf",
            "first_name": "jeremy",
            "last_name": "Trips",
            "noma": "14122",
            "student_card": File(open(os.path.join("static", "no_img.png"), "rb"))
        }
        self.client.post(reverse("create"), data=data)
    
    def verify_email(self, user_email):
        user = User.objects.get(email=user_email)
        token = EmailVerificationToken.objects.get(user_owner=user)
        self.client.post(reverse("verify_token"), data={
            "user_email": user_email,
            "token": token.token
        })

    def login(self, user_email):
        resp = self.client.post(reverse("login"), data={
            "email": user_email,
            "password": self.password
        })
        return resp.data["token"]

    def create_and_verify(self, user_email):
        self.createUser(user_email)
        self.verify_email(user_email)
        return User.objects.get(email=user_email)

    def create_and_verify_and_login(self, user_email):
        self.createUser(user_email)
        self.verify_email(user_email)
        user = User.objects.get(email=user_email)
        token = self.login(user_email)
        return user, token

    def test_report_user_serializer(self):
        """
        Test user serializer 
        """
        email1 = "orange@ciseau.be"
        email2 = "pierre@lune.be"
        user1, token = self.create_and_verify_and_login(email1)
        user2 = self.create_and_verify(email2)
        data ={
            "reason": "On est pas sorti du sable",
            "reported_user": 2
        }
        ser = UserReportSerializer(data=data)
        self.assertTrue(ser.is_valid())
        self.assertIn("reason", list(ser.validated_data))
        self.assertIn("reported_user", list(ser.validated_data))

    def test_report_user_serializer_with_error(self):
        """
        Test multiple user serializer errors
        """
        data = {
            "reson": "Allez vous couchez!",
            "reported_user": 1
        }
        ser = UserReportSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertIn("reason", ser.errors.keys())
        data = {
            "reason": "Allez vous couchez!",
            "reportsed_user": 1
        }
        ser = UserReportSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertIn("reported_user", ser.errors.keys())
        data = {
            "reason": "Allez vous couchez!",
            "reported_user": "Voucou"
        }
        ser = UserReportSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertEqual(ser.errors["reported_user"][0], "A valid integer is required.")

    def test_user_report_view(self):
        """
        Test user report view
        """
        email1 = "orange@ciseau.be"
        email2 = "pierre@lune.be"
        user1, token = self.create_and_verify_and_login(email1)
        user2 = self.create_and_verify(email2)
        resp = self.client.post(reverse("report"),
            data={
                "reason": "Moi, à une époque, je voulais faire vœu de pauvreté mais avec le pognon que j'rentrais, j'arrivais pas à concilier les deux.",
                "reported_user": 2
            },
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    
    def test_user_report_view_invalide_serializer(self):
        """
        test report view with invalid serializer
        """
        email1 = "orange@ciseau.be"
        email2 = "pierre@lune.be"
        user1, token = self.create_and_verify_and_login(email1)
        user2 = self.create_and_verify(email2)
        resp = self.client.post(reverse("report"),
            data={
                "reason": "Moi, à une époque, je voulais faire vœu de pauvreté mais avec le pognon que j'rentrais, j'arrivais pas à concilier les deux.",
                "reported_us": 2
            },
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_report_view_report_user_does_not_exist(self):
        """
        test report view when supplied user id does not exist
        """
        email1 = "orange@ciseau.be"
        user1, token = self.create_and_verify_and_login(email1)
        resp = self.client.post(reverse("report"),
            data={
                "reason": "Moi, à une époque, je voulais faire vœu de pauvreté mais avec le pognon que j'rentrais, j'arrivais pas à concilier les deux.",
                "reported_user": 2
            },
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data, ["REPORTED_USER_DOES_NOT_EXIST"])
        
    def test_report_with_not_email_verified(self):
        """
        Test report view when supplied user id is not email verified
        """
        email1 = "jai@tropdexam.com"
        email2 = "peutetre@tropdeprojet.be"
        user1, token = self.create_and_verify_and_login(email1)
        self.createUser(email2)
        resp = self.client.post(reverse("report"),
            data={
                "reason": "faut pas respirer la compote ça fait tousser",
                "reported_user": 2
            },
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data, ["REPORTED_USER_NOT_EMAIL_VERIFIED"])

    def test_report_user_while_not_authenticated(self):
        email1 = "jemappelle@henry.ru"
        email2 = "bebettethanru@truestory.com"
        self.createUser(email1)
        self.create_and_verify(email2)
        resp = self.client.post(reverse("report"),
            data={
                "reason": "faut pas respirer la compote ça fait tousser",
                "reported_user": 2
            }
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", resp.data.keys())
        self.assertEqual("Authentication credentials were not provided.", resp.data["detail"])

    def test_self_report_view(self):
        email1 = "jenaimare@defairedestest.com"
        user, token = self.create_and_verify_and_login(email1)
        resp = self.client.post(reverse("report"),
            data={
                "reason": "faut pas respirer la compote ça fait tousser",
                "reported_user": 1
            },
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data, ["SELF_REPORT_NOT_ALLOWED"])