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
        uri = '/shop/post/'
        request_data = {
            'title': '안녕하세요',
            'poster_name': '이진혁',
            'content': '어쩔티비 저쩔티비 우짤래미 저쩔래미 ^&^',
            'target_amount': 1000000,
            'final_date': '2023-04-26',  # component에서 DateCpnt로 date 유효성 검사
            'price': 15000
        }
        response = self.client.post(uri, request_data, format='json')
        self.assertEqual(response.status_code, 201, "성공")

        # serializer validation error
        request_data['poster_name'] = ''
        response = self.client.post(uri, request_data, format='json')
        self.assertEqual(response.status_code, 400, "blank 에러")

        # date관련 에러
        request_data["final_date"] = "2022-04-25"
        response = self.client.post(uri, request_data, format='json')
        self.assertEqual(response.status_code, 400, "date형 관련 에러")
