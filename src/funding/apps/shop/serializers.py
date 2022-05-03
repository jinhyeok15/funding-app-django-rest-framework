from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers

from funding.apps.user.serializers import UserSerializer
from .models import *
from funding.apps.user.models import User
from drf_yasg.utils import swagger_serializer_method
from funding.apps.core.components.date import DateComponent

from funding.apps.core.exceptions import CannotWriteError


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['target_amount']


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


class ShopPostMethod:
    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_all_funding_amount(self, obj):
        return obj.item.price * obj.participants.count()
    
    def get_d_day(self, obj):
        final_date_comp = DateComponent(obj.final_date)
        return final_date_comp.get_d_day()
    
    def get_success_rate(self, obj):
        all_funding_amount = self.get_all_funding_amount(obj)
        target_amount = obj.item.target_amount
        return (all_funding_amount/target_amount) * 100


class ShopPostDetailSerializer(ShopPostMethod, PostBaseSerializer):
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


class ShopPostsReadSerializer(ShopPostMethod, ModelSerializer):
    all_funding_amount = serializers.SerializerMethodField()
    d_day = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'title',
            'poster_name',
            'all_funding_amount',
            'success_rate',
            'd_day'
        ]


class ShopPostWriteSerializer(Serializer):
    poster_id = serializers.IntegerField()
    title = serializers.CharField()
    poster_name = serializers.CharField()
    content = serializers.CharField()
    target_amount = serializers.IntegerField()
    final_date = serializers.CharField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        target_amount = validated_data.get('target_amount')
        price = validated_data.get('price')
        item = Item.objects.create(target_amount=target_amount, price=price)

        poster = User.objects.get(pk=validated_data.get('poster_id'))
        title = validated_data.get('title')
        poster_name = validated_data.get('poster_name')
        content = validated_data.get('content')
        final_date = validated_data.get('final_date')
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
        instance.final_date = validated_data.get('final_date', instance.final_date)
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
