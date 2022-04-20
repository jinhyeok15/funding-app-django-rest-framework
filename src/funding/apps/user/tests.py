from django.test import TestCase, Client
from .models import User


class ProfileModelTests(TestCase):
    def setUp(self):
        User.objects.create(username="user1", email="user1@normal.user", password="user1")

    def test_user_register(self):
        user1 = User.objects.get(username="user1", password="user1")
        self.assertEqual(user1.email, "user1@normal.user")
