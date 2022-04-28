from django.db import models
from funding.apps.user.models import User
from funding.apps.core.models import PostBaseModel, PurchaseAbstractModel, TimeStampBaseModel
from funding.apps.core.validators import validate_final_date_component


class Item(TimeStampBaseModel):
    tag = models.CharField(max_length=256, null=True)
    price = models.IntegerField()
    target_amount = models.IntegerField()

    class Meta:
        db_table = 'shop_items'


class ShopPost(PostBaseModel):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    poster_name = models.CharField(max_length=50, blank=False)
    final_date = models.CharField(max_length=25, validators=[validate_final_date_component])
    status = models.CharField(max_length=12, default='FUNDING', help_text='''
        SUCCESS는 펀딩이 성공적으로 진행되어 상품 준비단계까지 진행된 상태이며, 
        FUNDING는 펀딩이 진행중인 상태, 
        CLOSE는 펀딩이 종료된 상태, 
        CANCEL는 펀딩 목표 금액을 넘지 못하여 펀딩이 취소된 상태를 의미한다. 
        결제는 DONATE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불된다.
    ''', choices=[
        ('SUCCESS', '성공'),
        ('FUNDING', '진행중'),
        ('CANCEL', '취소'),
        ('CLOSE', '펀딩종료')
    ])

    # ref: https://stackoverflow.com/questions/30752268/how-to-filter-objects-for-count-annotation-in-django
    def show_list(self):
        return self.objects.annotate(
            participants_count=models.Count('participants')
        )
    
    class Meta:
        db_table = 'shop_posts'


class ShopPurchase(PurchaseAbstractModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_purchases')
    production = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=[
        ('SUCCESS', '성공'),
        ('FAIL', '실패'),
        ('CANCEL', '취소/환불')
    ], default='SUCCESS')

    class Meta:
        db_table = 'shop_purchases'


class Participant(TimeStampBaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_join_logs')
    post_id = models.ForeignKey(ShopPost, on_delete=models.CASCADE, related_name='participants')
    purchase = models.OneToOneField(ShopPurchase, on_delete=models.CASCADE)
    is_join = models.BooleanField(default=True)

    class Meta:
        db_table = 'shop_participants'
