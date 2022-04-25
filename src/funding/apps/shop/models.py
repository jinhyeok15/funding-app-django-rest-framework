from django.db import models
from funding.apps.user.models import User
from funding.apps.core.models import PostBaseModel, PurchaseAbstractModel
from funding.apps.core.validators import validate_date_component


class Item(models.Model):
    tag = models.CharField(max_length=256, null=True)
    price = models.IntegerField()
    target_amount = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class ShopPost(PostBaseModel):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    poster_name = models.CharField(max_length=50, blank=False)
    final_date = models.CharField(max_length=25, validators=[validate_date_component])
    status = models.CharField(max_length=12, default='DONATE', help_text='''
        PURCHASE는 펀딩이 성공적으로 진행되어 상품 준비단계까지 진행된 상태이며, 
        DONATE는 펀딩에 참여하였으나 마감일이 끝나지 않은 상태, 
        CANCEL은 펀딩을 취소한 상태, 
        CLOSE는 펀딩 목표 금액을 넘지 못하여 펀딩이 취소된 상태를 의미한다. 
        결제는 DONATE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불된다.
    ''')

    # ref: https://stackoverflow.com/questions/30752268/how-to-filter-objects-for-count-annotation-in-django
    def show_list(self):
        return self.objects.annotate(
            participants_count=models.Count('participants')
        )


class ShopPurchase(PurchaseAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_purchases')
    production = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_join_logs')
    post = models.ForeignKey(ShopPost, on_delete=models.CASCADE, related_name='participants')
    purchase = models.OneToOneField(ShopPurchase, on_delete=models.CASCADE)
    is_join = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
