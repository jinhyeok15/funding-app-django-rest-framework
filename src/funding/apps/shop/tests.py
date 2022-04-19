from django.test import TestCase, Client
from .models import *


class ShopModelTests(TestCase):
    def setUp(self):
        self.item1 = Item(
            tag="item1", price=10000, target_amount=100000
        )
        self.item1.save()
        Item.objects.create(tag="item2", price=20000, target_amount=1000000)
    
    def test_get_item(self):
        item1 = self.item1
        item2 = Item.objects.get(id=2)
        self.assertEqual(item1.id, 1)
        self.assertEqual(item2.tag, "item2")


class ShopAPITests(TestCase):
    def test_create_item_post(self):
        c = Client()
        response = c.post('/shop/post/', {
            'title': '안녕하세요',
            'poster_name': '이진혁',
            'content': '어쩔티비 저쩔티비 우짤래미 저쩔래미 ^&^',
            'target_amount': 1000000,
            'final_date': '2022-04-26',  # component에서 DateBase로 date 유효성 검사
            'price': 15000
        })
        self.assertEqual(response.status_code, 200)
