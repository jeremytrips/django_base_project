from django.test import TestCase
from django.contrib.auth import get_user_model
import django

from .other_models.settings import Settings

# todo
"""
    LOGIN: with different user status
    LOGOUT: and check for token deleted
"""


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        settings = Settings.objects.create()
        user = User.objects.create_user(email='normal@user.com', password='foo', settings=settings)
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.settings.is_active)
        self.assertFalse(user.settings.is_admin)
        self.assertFalse(user.settings.is_staff)

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
        self.assertTrue(admin_user.settings.is_active)
        self.assertTrue(admin_user.settings.is_staff)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(django.db.utils.IntegrityError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', settings=settings)
