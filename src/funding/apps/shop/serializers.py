from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from funding.apps.core.models import ShopPostItemRequestModel
from .models import *


# It is to use optain request set in ShopPostItemView
class ShopPostItemRequestSerializer(ModelSerializer):
    title = serializers.CharField()
    poster_name = serializers.CharField()
    final_date = serializers.CharField()
    content = serializers.CharField()
    target_amount = serializers.IntegerField()
    price = serializers.IntegerField()

    class Meta:
        model = ShopPostItemRequestModel
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


class ShopPostSerializer(ModelSerializer):

    class Meta:
        model = ShopPost
        fields = '__all__'
