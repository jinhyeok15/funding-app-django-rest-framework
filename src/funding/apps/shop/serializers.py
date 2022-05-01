from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from funding.apps.user.serializers import UserSerializer
from .models import *
from drf_yasg.utils import swagger_serializer_method


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class ShopPostSerializer(ModelSerializer):
    item = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @swagger_serializer_method(serializer_or_field=ItemSerializer)
    def get_item(self, obj):
        return ItemSerializer(obj.item).data
    
    @swagger_serializer_method(serializer_or_field=UserSerializer)
    def get_poster(self, obj):
        return UserSerializer(obj.poster).data


class ShopPostCreateSerializer(ModelSerializer):
    """
    ## validation 목록
    * final_date
    DateComponentValidationError
    """

    class Meta:
        model = Post
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


class PurchaseCreateSerializer(ModelSerializer):

    class Meta:
        model = Purchase
        fields = ['user_id', 'production']


class ParticipantCreateSerializer(ModelSerializer):

    class Meta:
        model = Participant
        fields = [
            'user',
            'post_id',
            'purchase',
        ]
