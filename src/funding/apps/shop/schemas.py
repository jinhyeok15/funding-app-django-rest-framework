from drf_yasg import openapi
from drf_yasg.openapi import Schema, Parameter
from funding.apps.core.views import GenericResponse, HttpStatus
from pydantic import BaseModel


shop_post_item_logic = {
    'request_body': Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": Schema(type=openapi.TYPE_STRING),
            "poster_name": Schema(type=openapi.TYPE_STRING),
            "final_date": Schema(type=openapi.TYPE_STRING),
            "content": Schema(type=openapi.TYPE_STRING),
            "target_amount": Schema(type=openapi.TYPE_INTEGER),
            "price": Schema(type=openapi.TYPE_INTEGER)
        }
    ),
    "manual_parameters": [Parameter('Authorization', openapi.IN_HEADER, description="유저 토큰 -> Token {your token}", type=openapi.TYPE_STRING)],
    "responses": {
        201: Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "post_id": Schema(type=openapi.TYPE_INTEGER),
                "poster": Schema(type=openapi.TYPE_INTEGER),
                "item": Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        400: "serializer 에러"
    }
}
