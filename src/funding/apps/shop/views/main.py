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
    PostDoesNotExistError,
    SerializerValidationError,
    DoesNotExistedUserPocketError,
    UserAlreadyParticipateError,
    PostCannotParticipateError,
    PosterCannotParticipateError,
    UserCannotModifyPostError,
    CannotWriteError,
    UnsetPaginationError,
    NotFoundRequiredParameterError,
    PageBoundException,
    TargetAmountBoundException,
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

# utils
from funding.apps.core.utils import sorted_by, get_data_by_page

# redis-cache
from funding.apps.core.utils.backends.cache import (
    SHOP_POSTS_CREATED_DATA, 
    SHOP_POSTS_CREATED_DATA_STATUS, 
    cache, 
    SHOP_POSTS_DEFAULT_DATA, 
    SHOP_POSTS_DEFAULT_DATA_STATUS
)


class ShopPostItemView(ShopMixin, UserMixin, CoreMixin, APIView):

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
        
        except TargetAmountBoundException as e:
            return Response(None, HttpStatus(200, error=e))
        
        else:
            # end session
            transaction.savepoint_commit(sid)

            response_body = PostSerializer(post)

            return Response(response_body.data, HttpStatus(201, message="생성완료"))


class ShopWantParticipateView(ShopMixin, UserMixin, CoreMixin, APIView):
    
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


class ShopPostParticipateView(ShopMixin, CoreMixin, APIView):
    
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

    @swagger_auto_schema(**SHOP_POST_DETAIL_DELETE_LOGIC)
    @authorize
    def delete(self, request, user_id, post_id):
        try:
            self.validate_poster(user_id, post_id)
            self.delete_post(post_id)
        
        except PostDoesNotExistError as e:
            return Response(None, HttpStatus(404, error=e))
        
        else:
            return Response(None, HttpStatus(204))


class ShopPostsView(ShopMixin, CoreMixin, APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(**SHOP_POST_ITEM_READ_LOGIC)
    def get(self, request):
        try:
            query_string = request.GET

            search, order_by = (
                self.get_query_or_none(query_string, 'search'),
                self.get_query_or_exception(query_string, 'order_by'),
            )

            limit, offset = self.get_paginate_parameters(query_string)

            if order_by == 'default':
                # sorting에 시간이 소요되므로 default 데이터를 cache에 저장
                if cache.get(SHOP_POSTS_DEFAULT_DATA_STATUS):
                    data = cache.get(SHOP_POSTS_DEFAULT_DATA)
                else:
                    obj = self.read_posts(search=search)
                    data = sorted_by(
                        ShopPostsReadSerializer(obj, many=True).data,
                        key='all_funding_amount', reverse=True
                    )
                    cache.set(SHOP_POSTS_DEFAULT_DATA, data)
                    cache.set(SHOP_POSTS_DEFAULT_DATA_STATUS, True)
            elif order_by == 'created':
                if cache.get(SHOP_POSTS_CREATED_DATA_STATUS):
                    data = cache.get(SHOP_POSTS_CREATED_DATA)
                else:
                    obj = self.read_posts(search=search)
                    data = sorted_by(
                        ShopPostsReadSerializer(obj, many=True).data,
                        key='id', reverse=True
                    )
                    cache.set(SHOP_POSTS_CREATED_DATA, data)
                    cache.set(SHOP_POSTS_CREATED_DATA_STATUS, True)
            else:
                raise NotFoundRequiredParameterError('order_by')

            data = get_data_by_page(data, limit, offset)
        
        except UnsetPaginationError as e:
            return Response(None, HttpStatus(400, error=e))
        
        except NotFoundRequiredParameterError as e:
            return Response(None, HttpStatus(400, error=e))
        
        except PageBoundException as e:
            return Response(None, HttpStatus(400, error=e))

        else:
            return Response(data, HttpStatus(200, message="OK"))
