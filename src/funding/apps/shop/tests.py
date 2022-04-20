from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import *
from funding.apps.user.models import User


class ShopModelTests(TestCase):
    def setUp(self):
        self.item=Item.objects.create(tag="item2", price=20000, target_amount=1000000)

    def test_get_item(self):
        self.assertEqual(self.item.tag, "item2")


class ShopAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_create_item_post(self):
        response = self.client.post('/shop/post/', {
            'title': '안녕하세요',
            'poster_name': '이진혁',
            'content': '어쩔티비 저쩔티비 우짤래미 저쩔래미 ^&^',
            'target_amount': 1000000,
            'final_date': '2022-04-26',  # component에서 DateCpnt로 date 유효성 검사
            'price': 15000
        }, format='json')
        self.assertEqual(response.status_code, 200)
