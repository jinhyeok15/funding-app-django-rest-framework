from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from funding.apps.core.models import PostItemModel


# It is to use optain request set in PostItemView
class ShopPostItemSerializer(ModelSerializer):
    title = serializers.CharField()
    poster_name = serializers.CharField()
    final_date = serializers.CharField()
    content = serializers.CharField()
    target_amount = serializers.IntegerField()
    price = serializers.IntegerField()

    class Meta:
        model = PostItemModel
        fields = '__all__'


class ShopPostCreateSerializer(ModelSerializer):

    class Meta:
        model = ShopPost
        fields = [
            'item',
            'poster', 
            'title', 
            'content', 
            'poster_name', 
            'final_date'
        ]


class ItemCreateSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = [
            'price', 'target_amount'
        ]
