from drf_yasg import openapi
from drf_yasg.openapi import Schema, Parameter
from funding.apps.core.views import GenericResponse, HttpStatus
from pydantic import BaseModel
from rest_framework import status

from funding.apps.shop.serializers import ShopPostItemRequestSerializer, ShopPostSerializer


SHOP_POST_ITEM_CREATE_LOGIC = {
    'request_body': ShopPostItemRequestSerializer,
    "manual_parameters": [
        Parameter('Authorization', openapi.IN_HEADER, description="유저 토큰 -> Token {your token}", type=openapi.TYPE_STRING)
    ],
    "responses": {
        201: ShopPostSerializer,
        400: Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "code": Schema(type=openapi.TYPE_INTEGER),
                "status": Schema(title=status.HTTP_400_BAD_REQUEST, type=openapi.TYPE_STRING)
            }
        )
    }
}
