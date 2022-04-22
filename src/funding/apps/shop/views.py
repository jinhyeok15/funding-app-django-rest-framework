# GenericAPIView 사용 이유
# https://stackoverflow.com/questions/42311888/django-rest-swagger-apiview
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
# 트랜잭션 참조
# https://docs.djangoproject.com/en/3.0/topics/db/transactions/#django.db.transaction.atomic
from django.db import transaction
from django.core.exceptions import ValidationError
from funding.apps.core.views import (
    IntegrationMixin,
    InheritedResponse as Response, HttpStatus
)


class ShopPostItemView(IntegrationMixin, GenericAPIView):
    """
    request로 부터 header를 가져와서 User obj 가져오기
    request.data 내부에서 Item 요소를 가져와 Item obj를 생성한다.
    PostCreateSerializer를 생성하고, validation 진행 후 save한다.
    Response 데이터로 post_id, user, item을 반환한다.
    """
    
    serializer_class = PostItemSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_valid_szr(PostItemSerializer, data=request.data)
        except ValidationError:
            return Response(serializer.errors, HttpStatus(400, 
            """
            Not valid request body please check client form
            """))

        poster_id = self.get_auth_user(request)

        # create session
        sid = transaction.savepoint()
        try:
            serializer = self.get_valid_szr(
                ItemCreateSerializer, data={
                    'price': request.data['price'],
                    'target_amount': request.data['target_amount']
                }
            )
            item = serializer.save()

            serializer = self.get_valid_szr(
                PostCreateSerializer, data={
                    'item': item.id,
                    'poster': poster_id,
                    'title': request.data['title'],
                    'content': request.data['content'],
                    'poster_name': request.data['poster_name'],
                    'final_date': request.data['final_date']
                }
            )
            post = serializer.save()
        except ValidationError:
            transaction.savepoint_rollback(sid)
            return Response(serializer.errors, HttpStatus(400, 
            """
            유효하지 않은 값이 있어 DB에 저장할 수 없습니다
            """))
        # end session
        transaction.savepoint_commit(sid)

        return Response({
            "post_id": post.id,
            "poster": poster_id,
            "item": item.id
        }, HttpStatus(201, message="생성완료"))
