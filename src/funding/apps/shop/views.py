from rest_framework.views import APIView
from .serializers import *
from .schemas import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
# 트랜잭션 참조
# https://docs.djangoproject.com/en/3.0/topics/db/transactions/#django.db.transaction.atomic
from django.db import transaction
from funding.apps.core.exceptions import SerializerValidationError
from funding.apps.core.views import (
    IntegrationMixin,
    GenericResponse as Response, HttpStatus
)
from drf_yasg.utils import swagger_auto_schema


class ShopPostItemView(IntegrationMixin, APIView):
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

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        **SHOP_POST_ITEM_CREATE_LOGIC
    )
    @transaction.atomic()
    def post(self, request, *args, **kwargs):

        poster_id = self.get_auth_user(request)

        # create session
        sid = transaction.savepoint()
        try:
            serializer = self.get_valid_szr(
                ItemCreateSerializer, data=request.data
            )
            item = serializer.save()

            serializer = self.get_valid_szr(
                ShopPostCreateSerializer, data={
                    **request.data,
                    'item': item.id,
                    'poster': poster_id
                }
            )
            post = serializer.save()
        except SerializerValidationError as e:
            transaction.savepoint_rollback(sid)
            return Response(None, HttpStatus(400, error=e))
        # end session
        transaction.savepoint_commit(sid)

        response_body = ShopPostSerializer(post)

        return Response(response_body.data, HttpStatus(201, message="생성완료"))
