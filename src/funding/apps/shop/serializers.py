from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from funding.apps.abstract.models import AbstractPostItem


# It is to use optain request set in PostItemView
class PostItemSerializer(ModelSerializer):
    title = serializers.CharField()
    poster_name = serializers.CharField()
    final_date = serializers.CharField()
    content = serializers.CharField()
    target_amount = serializers.IntegerField()
    price = serializers.IntegerField()

    class Meta:
        model = AbstractPostItem
        fields = '__all__'


class PostCreateSerializer(ModelSerializer):

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


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = [
            'tag', 'price', 'target_amount', 'updated_at'
        ]
        read_only_fields = ['target_amount', 'updated_at']
