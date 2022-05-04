from rest_framework.views import APIView
from uritemplate import partial

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
    PostDoesNotExistError,
    SerializerValidationError,
    DoesNotExistedUserPocketError,
    UserAlreadyParticipateError,
    PostCannotParticipateError,
    PosterCannotParticipateError,
    UserCannotModifyPostError,
    CannotWriteError,
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

        # create session
        sid = transaction.savepoint()

        try:
            self.get_valid_user_pocket(poster_id)

            serializer = self.get_valid_szr(
                ShopPostWriteSerializer, data={"poster_id": poster_id, **request.data}
            )
            post = serializer.save()

        except SerializerValidationError as e:
            transaction.savepoint_rollback(sid)
            return Response(None, HttpStatus(400, error=e))

        except DoesNotExistedUserPocketError as e:
            return Response(None, HttpStatus(200, error=e))
        
        else:
            # end session
            transaction.savepoint_commit(sid)

            response_body = PostSerializer(post)

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
        try:
            self.validate_unparticipated_user(user_id, post_id)
            self.validate_user_not_poster(user_id, post_id)
            pocket = self.get_valid_user_pocket(user_id)
            response_body = UserPocketSerializer(pocket)

        except DoesNotExistedUserPocketError as e:
            return Response(None, HttpStatus(200, error=e))

        except UserAlreadyParticipateError as e:
            return Response(None, HttpStatus(400, error=e))
        
        except PosterCannotParticipateError as e:
            return Response(None, HttpStatus(400, error=e))
        
        else:
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
        
        else:
            # end session
            transaction.savepoint_commit(sid)
            
            return Response(None, HttpStatus(200, "OK"))


class ShopPostDetailView(CoreMixin, ShopMixin, APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(**SHOP_POST_DETAIL_READ_LOGIC)
    def get(self, request, post_id):
        try:
            post = self.get_active_post(post_id)
            serializer = ShopPostDetailSerializer(post)
        
        except PostDoesNotExistError as e:
            return Response(None, HttpStatus(404, error=e))
        
        else:
            return Response(serializer.data, HttpStatus(200, "OK"))

    @swagger_auto_schema(**SHOP_POST_DETAIL_UPDATE_LOGIC)
    @authorize
    @transaction.atomic()
    def patch(self, request, user_id, post_id):

        sid = transaction.savepoint()

        try:
            self.validate_poster(user_id, post_id)

            post = self.get_active_post(post_id)
            self.get_valid_szr(
                ShopPostWriteSerializer, instance=post, data=request.data, partial=True
            ).save()

        except SerializerValidationError as e:
            transaction.savepoint_rollback(sid)
            return Response(None, HttpStatus(400, error=e))
        
        except PostDoesNotExistError as e:
            return Response(None, HttpStatus(404, error=e))
        
        except UserCannotModifyPostError as e:
            return Response(None, HttpStatus(400, error=e))
        
        except CannotWriteError as e:
            return Response(None, HttpStatus(400, error=e))
        
        else:
            # end session
            transaction.savepoint_commit(sid)
            
            return Response(None, HttpStatus(201, "수정완료"))

    @swagger_auto_schema()
    @authorize
    def delete(self, request, user_id, post_id):
        try:
            self.validate_poster(user_id, post_id)
            self.delete_post(post_id)
        
        except PostDoesNotExistError as e:
            return Response(None, HttpStatus(404, error=e))
        
        else:
            return Response(None, HttpStatus(204))
