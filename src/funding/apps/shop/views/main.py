from rest_framework.views import APIView

# serializers
from ..serializers import *
from funding.apps.user.serializers import (
    PocketSerializer as UserPocketSerializer
)

# API swagger schema
from ..schemas import *
from drf_yasg.utils import swagger_auto_schema

# user permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from funding.apps.core.views.decorators import authorize

# transaction
from django.db import transaction

# exceptions
from funding.apps.core.exceptions import (
    SerializerValidationError,
    DoesNotExistedUserPocketError,
    UserAlreadyParticipateError,
    PostCannotParticipateError,
    PosterCannotParticipateError
)

# response
from funding.apps.core.views.response import (
    GenericResponse as Response, HttpStatus,
)

# views mixins
from .mixins import (
    ShopMixin
)
from funding.apps.core.views.mixins import CoreMixin
from funding.apps.user.views.mixins import UserMixin


class ShopPostItemView(
    ShopMixin,
    UserMixin,
    CoreMixin,
    APIView
):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SHOP_POST_ITEM_CREATE_LOGIC)
    @authorize
    @transaction.atomic()
    def post(self, request, poster_id):
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

        # create session
        sid = transaction.savepoint()

        try:
            self.get_valid_user_pocket(poster_id)

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

        except DoesNotExistedUserPocketError as e:
            transaction.savepoint_rollback(sid)
            return Response(None, HttpStatus(200, error=e))

        # end session
        transaction.savepoint_commit(sid)

        response_body = ShopPostSerializer(post)

        return Response(response_body.data, HttpStatus(201, message="생성완료"))


class ShopWantParticipateView(
    ShopMixin,
    UserMixin,
    CoreMixin,
    APIView
):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SHOP_WANT_PARTICIPATE_LOGIC)
    @authorize
    def get(self, request, user_id, post_id):
        """
        # 펀딩 상품 참여 가능 여부 체크 API

        ## 개요

        - 펀딩 참여하기 버튼을 눌렀을 때, 상품 결제 창으로 옮겨진다.

        - 결제 창으로 옮겨지기 전 해당 API를 통해 유저의 결제 상태를 체크한다.

        ## 필수요건
        
        1. 유저 지갑 개설 여부 조회(is_active) 후, 개설이 되어 있을 경우 결제 진행.
    
        2. 유저가 이미 참여를 한 경우 400 ValidationError
        """

        try:
            self.validate_unparticipated_user(user_id, post_id)
            pocket = self.get_valid_user_pocket(user_id)
            response_body = UserPocketSerializer(pocket)

        except DoesNotExistedUserPocketError as e:
            return Response(None, HttpStatus(200, error=e))

        except UserAlreadyParticipateError as e:
            return Response(None, HttpStatus(400, error=e))

        return Response({"pocket":response_body.data}, HttpStatus(200, "OK"))


class ShopPostParticipateView(
    ShopMixin,
    CoreMixin,
    APIView
):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SHOP_POST_PARTICIPATE_LOGIC)
    @authorize
    @transaction.atomic()
    def post(self, request, user_id, post_id):
        """
        # 펀딩 상품 참여 등록 API

        ## 개요

        - 유저가 결제를 성공할 경우에, 결제 내역을 기록하고, 유저 참여 여부를 등록한다.

        ## 필수요건

        1. 유저가 이미 참여를 한 경우 400 ValidationError
        2. 유저가 아닌 게시자의 경우 참여 불가
        3. 결제 내역 기록, 유저 참여 여부 등록 transaction 구성
        """

        sid = transaction.savepoint()

        try:
            self.validate_unparticipated_user(user_id, post_id)
            self.validate_user_not_poster(user_id, post_id)

            item = self.get_item_by_post_id_to_participate(post_id)
            purchase = self.get_valid_szr(PurchaseCreateSerializer, data={
                "user_id": user_id, "production": item.id
            }).save()
            self.get_valid_szr(ParticipantCreateSerializer, data={
                "user": user_id,
                "post_id": post_id,
                "purchase": purchase.id
            }).save()

        except UserAlreadyParticipateError as e:
            return Response(None, HttpStatus(400, error=e))

        except PostCannotParticipateError as e:
            return Response(None, HttpStatus(400, error=e))
        
        except PosterCannotParticipateError as e:
            return Response(None, HttpStatus(400, error=e))

        except SerializerValidationError as e:
            transaction.savepoint_rollback(sid)
            return Response(None, HttpStatus(400, error=e))
        
        return Response(None, HttpStatus(200, "OK"))
