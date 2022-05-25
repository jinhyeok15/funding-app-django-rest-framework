from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from funding.apps.user.serializers import UserSerializer

from ..models import *
from funding.apps.user.models import User

# swagger_serializer_method
from drf_yasg.utils import swagger_serializer_method

# utils
from funding.apps.core.utils.components import money, date, Money
from funding.apps.core.utils import sorted_by

#exceptions
from funding.apps.core.exceptions import (
    CannotWriteError,
    NotFoundRequiredParameterError
)

# validators for serializer
from .validators import *

# redis-cache
from funding.apps.core.utils.backends.cache import (
    SHOP_POSTS_CREATED_DATA, 
    cache, 
    SHOP_POSTS_DEFAULT_DATA, 
)


class ItemSerializer(ModelSerializer):
    price = serializers.SerializerMethodField()
    target_amount = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['target_amount']
    
    def get_price(self, obj) -> str:
        return money(obj.price).value_of(str)
    
    def get_target_amount(self, obj) -> str:
        return money(obj.target_amount).value_of(str)


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostBaseSerializer(PostSerializer):
    item = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=ItemSerializer)
    def get_item(self, obj):
        return ItemSerializer(obj.item).data
    
    @swagger_serializer_method(serializer_or_field=UserSerializer)
    def get_poster(self, obj):
        return UserSerializer(obj.poster).data


class ShopPostMixin:
    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_all_funding_amount(self, obj) -> str:
        return money(obj.item.price).times(obj.participants.count()).value_of(str)
    
    def get_d_day(self, obj):
        final_date_comp = date.DateComponent(obj.final_date)
        return final_date_comp.get_d_day()
    
    def get_success_rate(self, obj):
        all_funding_amount = money(self.get_all_funding_amount(obj)).value_of(int)
        target_amount = obj.item.target_amount
        return int((all_funding_amount/target_amount) * 100)


class ShopPostDetailSerializer(ShopPostMixin, PostBaseSerializer):
    participant_count = serializers.SerializerMethodField()
    all_funding_amount = serializers.SerializerMethodField()
    d_day = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'poster',
            'title',
            'content',
            'item',
            'poster_name',
            'status',
            'participant_count',
            'all_funding_amount',
            'success_rate',
            'd_day'
        ]


class ShopPostsReadSerializer(ShopPostMixin, ModelSerializer):
    all_funding_amount = serializers.SerializerMethodField()
    d_day = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'poster_name',
            'all_funding_amount',
            'success_rate',
            'd_day',
            'status'
        ]
    
    @classmethod
    def get_sorted_data(cls, obj, order_by):
        serializer_data = cls(obj, many=True).data
        if order_by == 'default':
            data = sorted_by(
                serializer_data,
                key='all_funding_amount', component=Money, reverse=True
            )
            cache.set(SHOP_POSTS_DEFAULT_DATA, data)
        elif order_by == 'created':
            data = sorted_by(
                serializer_data,
                key='id', reverse=True
            )
            cache.set(SHOP_POSTS_CREATED_DATA, data)
        else:
            raise NotFoundRequiredParameterError('order_by')
        
        data = sorted_by(
                    data, key='status', component=PostStatusComponent
                )
        return data


class ShopPostWriteSerializer(Serializer):
    poster_id = serializers.IntegerField()
    title = serializers.CharField()
    poster_name = serializers.CharField()
    content = serializers.CharField()
    target_amount = serializers.IntegerField()
    final_date = serializers.CharField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        target_amount = validate_target_amount(validated_data.get('target_amount'))
        price = validated_data.get('price')
        item = Item.objects.create(target_amount=target_amount, price=price)

        poster = User.objects.get(pk=validated_data.get('poster_id'))
        title = validated_data.get('title')
        poster_name = validated_data.get('poster_name')
        content = validated_data.get('content')
        final_date = validate_final_date(
            validated_data.get('final_date')
        )

        post = Post.objects.create(item=item, poster=poster,
            title=title,
            poster_name=poster_name,
            content=content,
            final_date=final_date
        )

        return post
    
    def update(self, instance, validated_data):
        target_amount = validated_data.get('target_amount', None)
        if target_amount is not None:
            raise CannotWriteError({
                "target_amount": target_amount
            })
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.poster_name = validated_data.get('poster_name', instance.poster_name)
        instance.final_date = validate_final_date(validated_data.get('final_date', instance.final_date))
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        instance.item.price = validated_data.get('price', instance.item.price)
        instance.item.save()

        return instance


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
