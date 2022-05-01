import json
from drf_yasg import openapi
from drf_yasg.openapi import *
from drf_yasg.openapi import Parameter
from funding.apps.core.views import get_status_by_code, GenericResponse as Response, HttpStatus
from funding.apps.shop.serializers import ShopPostSerializer
from funding.apps.user.serializers import PocketSerializer
from funding.apps.core.exceptions import (
    DoesNotExistedUserPocketError,
    UserAlreadyParticipateError
)

AUTH_TOKEN_PARAMETER = Parameter('Authorization', openapi.IN_HEADER, description="유저 토큰 -> Token {your token}", type=openapi.TYPE_STRING)
POST_ID_PATH_PARAMETER = Parameter("post_id", IN_PATH, required=True, type=TYPE_INTEGER)


SHOP_POST_ITEM_CREATE_LOGIC = {
    "request_body": Schema(
        type=TYPE_OBJECT,
        properties={
            "title": Schema(title="제목", type=TYPE_STRING),
            "poster_name": Schema(
                title="게시자 이름",
                description="게시자 이름과 유저의 이름은 다를 수 있음",
                type=TYPE_STRING
            ),
            "content": Schema(
                title="펀딩 아이템 소개 컨텐츠",
                type=TYPE_STRING
            ),
            "target_amount": Schema(
                title="목표 금액",
                type=TYPE_INTEGER
            ),
            "final_date": Schema(
                title="종료일",
                type=TYPE_STRING
            ),
            "price": Schema(
                title="아이템 가격",
                type=TYPE_INTEGER
            )
        }
    ),
    "manual_parameters": [
        AUTH_TOKEN_PARAMETER
    ],
    "responses": {
        201: ShopPostSerializer,
        400: get_status_by_code(400),
        200: DoesNotExistedUserPocketError.status,
        401: get_status_by_code(401)
    }
}


SHOP_WANT_PARTICIPATE_LOGIC = {
    "manual_parameters": [
        POST_ID_PATH_PARAMETER,
        AUTH_TOKEN_PARAMETER
    ],
    "responses": {
        200: PocketSerializer,
        400: UserAlreadyParticipateError.status,
        401: get_status_by_code(401),
        200: DoesNotExistedUserPocketError.status
    }
}


SHOP_POST_PARTICIPATE_LOGIC = {
    "manual_parameters": [
        POST_ID_PATH_PARAMETER,
        AUTH_TOKEN_PARAMETER
    ],
    "responses": {
        200: get_status_by_code(200),
        401: get_status_by_code(401),
        400: get_status_by_code(400)
    }
}


SHOP_POST_DETAIL_READ_LOGIC = {
    "manual_parameters": [
        POST_ID_PATH_PARAMETER,
        AUTH_TOKEN_PARAMETER
    ],
    "responses": {
        200: "조회완료",
        401: get_status_by_code(401),
    }
}
