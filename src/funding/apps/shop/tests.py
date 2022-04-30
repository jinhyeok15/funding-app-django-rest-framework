from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import *
from funding.apps.user.models import User, Pocket
from funding.apps.core.exceptions import DoesNotIncludeStatusError


class ShopModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.item = Item.objects.create(
            tag="cheeze",
            price=4500,
            target_amount=600000
        )
        self.item=Item.objects.create(tag="item2", price=20000, target_amount=1000000)
        self.purchase = Purchase.objects.create(
            user_id=self.user,
            production=self.item
        )
    
    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_item(self):
        self.assertEqual(self.item.tag, "item2")
    
    def test_Purchase_get(self):
        self.assertRaises(DoesNotIncludeStatusError, Purchase.objects.get, pk=self.purchase.id)


class ShopAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

        self.item = Item.objects.create(
            tag="cheeze",
            price=4500,
            target_amount=600000
        )
        self.post = Post.objects.create(
            poster=self.user,
            title="hi hi hi",
            content="nice to meet you",
            item=self.item,
            poster_name="jj",
            final_date="2022.07.10"
        )
    
    def tearDown(self) -> None:
        return super().tearDown()

    def test_ShopPostItemView_post(self):
        uri = '/shop/v1/post/'
        request_data = {
            'title': '안녕하세요',
            'poster_name': '이진혁',
            'content': '어쩔티비 저쩔티비 우짤래미 저쩔래미 ^&^',
            'target_amount': 1000000,
            'final_date': '2023-04-26',  # component에서 DateCpnt로 date 유효성 검사
            'price': 15000
        }
        response = self.client.post(uri, request_data, format='json')
        self.assertEqual(response.status_code, 422, "422 fail")

        Pocket.objects.get(user_id=self.user.id, is_active=False).update(bank_account_type="NH", is_active=True)
        response = self.client.post(uri, request_data, format='json')
        self.assertEqual(response.status_code, 201, "201 fail")

        # serializer validation error
        request_data['poster_name'] = ''
        response = self.client.post(uri, request_data, format='json')
        self.assertEqual(response.status_code, 400, "400 serializer error fail")

        # date관련 에러
        request_data["final_date"] = "2022-04-25"
        response = self.client.post(uri, request_data, format='json')
        self.assertEqual(response.status_code, 400, "400 date형 관련 에러 fail")
    
    def test_ShopWantParticipateView_get(self):
        uri = f'/shop/v1/{self.post.id}/want_participate/'
        partner = User.objects.create_user('partner1', 'partner1@partner.com', 'partner123')
        ptoken = Token.objects.create(user=partner)
        partner_client = APIClient()
        partner_client.credentials(HTTP_AUTHORIZATION='Token '+ptoken.key)

        # 422 test
        response = partner_client.get(uri)
        self.assertEqual(response.status_code, 422, "422 fail")

        # 200 test
        Pocket.objects.get(user_id=partner.id, is_active=False).update(bank_account_type="NH", is_active=True)
        response = partner_client.get(uri)
        self.assertEqual(response.status_code, 200, "200 fail")

        # 400 test
        purchase=Purchase.objects.create(
            user_id=partner,
            production=self.item
        )
        Participant.objects.create(
            user=partner,
            post_id=self.post,
            purchase=purchase
        )
        response = partner_client.get(uri)
        self.assertEqual(response.status_code, 400, "400 fail")
