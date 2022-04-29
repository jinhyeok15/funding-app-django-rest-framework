from rest_framework.views import APIView
from .serializers import *
from .schemas import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
# 트랜잭션 참조
# https://docs.djangoproject.com/en/3.0/topics/db/transactions/#django.db.transaction.atomic
from django.db import transaction
from funding.apps.core.exceptions import (
    SerializerValidationError,
    DoesNotExistedUserPocketError
)
from funding.apps.core.views import (
    IntegrationMixin,
    GenericResponse as Response, HttpStatus
)
from drf_yasg.utils import swagger_auto_schema


class ShopPostItemView(IntegrationMixin, APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SHOP_POST_ITEM_CREATE_LOGIC)
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        # 펀딩 게시글 생성 API v1.0.0

        ## 개요

        - 펀딩 게시글 생성 API

        ## 필수요건

        1. request로 부터 header를 가져와서 User obj 가져오기

        2. request.data 내부에서 Item 요소를 가져와 Item obj를 생성한다.

        3. PostCreateSerializer를 생성하고, validation 진행 후 save한다.

        4. Response 데이터로 post_id, user, item을 반환한다.

        ## 구현설명

        게시자가 Item과 관련한 게시물을 작성한다는 점을 고려하여, Item과 Post 관련한 부분을 분리하였습니다. 
        Funding shop 도메인에서는 Item이 핵심인 게시물이겠지만, 이후 커뮤니티로 발전할 경우와 같은 게시물의 확장성을 고려하였습니다. 
        이렇게 될 경우, 단순히 게시물을 CREATE하는 API가 아닌, 게시자가 Item을 먼저 등록한 후 이를 게시한다는 논리 구조가 형성됩니다. 
        이를 View에서 비즈니스 로직으로 구현하기 위해 두 개의 테이블에 접근하여 create하는 트랜잭션을 관리할 세션을 django.db.transaction 모듈을 통해 생성하였습니다.  

        또한 request.data를 validation할 PostItemSerializer의 경우, AbstractPostItem model을 받아서 기존 모델(Item, ShopPost)와 형식이 맞지 않아 에러가 나는 부분을 해결했습니다.  

        response에서는 client에서 사용할 게시물 id와 게시자 id, item id를 제공하여 client 측에서 접근할 수 있도록 하였습니다.
        """

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


class ShopPostPurchaseView(IntegrationMixin, APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SHOP_POST_PURCHASE_CREATE_LOGIC)
    def post(self, request, *args, **kwargs):
        """
        # 펀딩 상품 구매하기 API

        ## 개요

        - 펀딩 참여하기 버튼을 눌렀을 때, 상품 결제 창으로 옮겨진다.

        - 결제하기 버튼을 최종적으로 눌렀을 때, 해당 API가 불려진다.

        - 게시글에 올린 상품을 구매

        - 구매 이후 participant API 호출

        ## 필수요건
        
        1. 유저 지갑 개설 여부 조회(is_active) 후, 개설이 되어 있을 경우 결제 진행.
        (단 이 부분을 요청하는 API를 따로 떼서 참여하기 버튼을 클릭했을 시에 검증이 ~들어갈 수도 있음~ -> API 필요: 한 사람이 한번만 참여 가능)
    
        2. 지갑에 있는 금액보다 상품 금액이 크면 결제가 불가능하다. 이 부분에 대해 Validation 검증 들어가야 함.
        """

        user_id = self.get_auth_user(request)

        try:
            pocket = self.get_valid_user_pocket(user_id)
        except DoesNotExistedUserPocketError as e:
            return Response(None, http=HttpStatus(422, error=e))

        return Response(data=None, http=HttpStatus(200, "NOT_CREATED"))
