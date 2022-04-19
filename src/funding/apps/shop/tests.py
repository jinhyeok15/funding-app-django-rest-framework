from django.test import TestCase
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
