from django.test import TestCase, Client
from .models import User


class UserModelTests(TestCase):
    def setUp(self):
        User.objects.create(username="user1", email="user1@normal.user", password="user1")

    def test_user_register(self):
        user1 = User.objects.get(username="user1", password="user1")
        self.assertEqual(user1.email, "user1@normal.user")


class UserAPITests(TestCase):
    def test_account_signup(self):
        c = Client()
        response = c.post(
            '/account/signup/', {
                'username': '진혁이',
                'email': 'fhfhfh@email.com',
                'password': '12345678'
            }
        )
        self.assertEqual(response.status_code, 201)
        response = c.post(
            '/account/signup/', {
                'username': '진혁 이',
                'email': 'fhfhfh@email.com',
                'password': '12345678'
            }
        )
        self.assertEqual(response.status_code, 400)
