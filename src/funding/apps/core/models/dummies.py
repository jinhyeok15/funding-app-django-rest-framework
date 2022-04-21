from django.db import models


class PostItemModel(models.Model):
    title: models.CharField
    poster_name: models.CharField
    final_date: models.CharField
    content: models.TextField
    target_amount: models.IntegerField
    price: models.IntegerField
