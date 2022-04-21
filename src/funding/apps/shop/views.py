# GenericAPIView 사용 이유
# https://stackoverflow.com/questions/42311888/django-rest-swagger-apiview
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
# 트랜잭션 참조
# https://docs.djangoproject.com/en/3.0/topics/db/transactions/#django.db.transaction.atomic
from django.db import transaction


class PostItem(GenericAPIView):
    serializer_class = PostItemSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = PostItemSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # request로 부터 header를 가져와서 User obj 가져오기
        # request.data 내부에서 Item 요소를 가져와 Item obj를 생성한다.
        # PostCreateSerializer를 생성하고, validation 진행 후 save한다.
        # Response 데이터로 post_id, user, item을 반환한다.

        token_key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = Token.objects.get(key=token_key)
        poster_id = token.user_id

        # create session
        sid = transaction.savepoint()
        item_serializer = ItemCreateSerializer(data={
            'price': request.data['price'],
            'target_amount': request.data['target_amount']
        })
        if item_serializer.is_valid() is False:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        item = item_serializer.save()

        post_serializer = PostCreateSerializer(data={
            'item': item.id,
            'poster': poster_id,
            'title': request.data['title'],
            'content': request.data['content'],
            'poster_name': request.data['poster_name'],
            'final_date': request.data['final_date']
        })
        if post_serializer.is_valid() is False:
            transaction.savepoint_rollback(sid)
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post = post_serializer.save()
        # end session
        transaction.savepoint_commit(sid)

        return Response({
            "post_id": post.id,
            "poster": poster_id,
            "item": item.id
        }, status=status.HTTP_200_OK)
