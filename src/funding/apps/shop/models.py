from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from funding.apps.profile.models import User
from funding.apps.abstract.models import Post, PurchaseInterface


class Item(models.Model):
    tag = models.CharField(max_length=256, null=True)
    price = models.IntegerField()
    target_amount = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class ShopPost(Post):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    poster_name = models.CharField(max_length=50)
    final_date = models.CharField(max_length=25)

    # ref: https://stackoverflow.com/questions/30752268/how-to-filter-objects-for-count-annotation-in-django
    def show_list(self):
        return self.objects.annotate(
            participants_count=models.Count('participants')
        )


class ShopPurchase(PurchaseInterface):
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
