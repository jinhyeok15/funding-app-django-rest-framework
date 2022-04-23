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
    post:

    request로 부터 header를 가져와서 User obj 가져오기
    request.data 내부에서 Item 요소를 가져와 Item obj를 생성한다.
    PostCreateSerializer를 생성하고, validation 진행 후 save한다.
    Response 데이터로 post_id, user, item을 반환한다.

    * Description

    게시자가 Item과 관련한 게시물을 작성한다는 점을 고려하여, Item과 Post 관련한 부분을 분리하였습니다. 
    Funding shop 도메인에서는 Item이 핵심인 게시물이겠지만, 이후 커뮤니티로 발전할 경우와 같은 게시물의 확장성을 고려하였습니다. 
    이렇게 될 경우, 단순히 게시물을 CREATE하는 API가 아닌, 게시자가 Item을 먼저 등록한 후 이를 게시한다는 논리 구조가 형성됩니다. 
    이를 View에서 비즈니스 로직으로 구현하기 위해 두 개의 테이블에 접근하여 create하는 트랜잭션을 관리할 세션을 django.db.transaction 모듈을 통해 생성하였습니다.  

    또한 request.data를 validation할 PostItemSerializer의 경우, AbstractPostItem model을 받아서 기존 모델(Item, ShopPost)와 형식이 맞지 않아 에러가 나는 부분을 해결했습니다.  

    response에서는 client에서 사용할 게시물 id와 게시자 id, item id를 제공하여 client 측에서 접근할 수 있도록 하였습니다.
    """
    serializer_class = PostItemSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_valid_szr(PostItemSerializer, data=request.data)
        except ValidationError as e:
            return Response(None, HttpStatus(400, error=e))

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
        except ValidationError as e:
            transaction.savepoint_rollback(sid)
            return Response(None, HttpStatus(400, error=e))
        # end session
        transaction.savepoint_commit(sid)

        return Response({
            "post_id": post.id,
            "poster": poster_id,
            "item": item.id
        }, HttpStatus(201, message="생성완료"))
