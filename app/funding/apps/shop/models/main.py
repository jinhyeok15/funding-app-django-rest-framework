from django.db import models
from funding.apps.user.models import User
from funding.apps.core.models import (
    PostBaseModel,
    PurchaseAbstractModel,
    TimeStampBaseModel,
    ItemBaseModel
)
from .managers import *


class Item(ItemBaseModel):
    target_amount = models.IntegerField()

    class Meta:
        db_table = 'shop_items'


class Post(PostBaseModel):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    poster_name = models.CharField(max_length=50)
    final_date = models.CharField(max_length=25)
    status = models.CharField(max_length=12, default='FUNDING', help_text='''
        SUCCESS는 펀딩이 성공적으로 진행되어 상품 준비단계까지 진행된 상태이며, 
        FUNDING는 펀딩이 진행중인 상태, 
        CLOSE는 펀딩이 종료된 상태, 
        CANCEL는 게시자가 확인되지 않아 글 작성이 취소된 상태이다.
        결제는 DONATE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불된다.
    ''', choices=[
        ('SUCCESS', '성공'),
        ('FUNDING', '진행중'),
        ('CANCEL', '취소'),
        ('CLOSE', '펀딩종료'),
    ])
    objects = ShopPostManager()
    
    class Meta:
        db_table = 'shop_posts'


class PostStatusComponent:
    ORDER = {
        'FUNDING': 0,
        'SUCCESS': 1,
        'CLOSE': 2,
        'CANCEL': 4
    }
    def __init__(self, value):
        self.value = value
        self.order_tag = self.ORDER[self.value]
    
    def compare_of(self, a):
        try:
            if self.order_tag > a.order_tag:
                return 1
            elif self.order_tag < a.order_tag:
                return -1
            elif self.order_tag == a.order_tag:
                return 0
        except:
            raise ValueError


class Purchase(PurchaseAbstractModel):
    STATUS_CHOICES = [
        ('SUCCESS', '성공'),
        ('FAIL', '실패'),
        ('CANCEL', '취소/환불')
    ]
    STATUS_DEFAULT = 'SUCCESS'

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_purchases', db_column='user_id')
    production = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_DEFAULT)

    class Meta:
        db_table = 'shop_purchases'


class Participant(TimeStampBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_join_logs', db_column='user_id')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='participants', db_column='post_id')
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    is_join = models.BooleanField(default=True)

    class Meta:
        db_table = 'shop_participants'
