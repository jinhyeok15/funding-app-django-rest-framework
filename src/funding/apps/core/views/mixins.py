from rest_framework.authtoken.models import Token
from rest_framework.fields import empty
from ..exceptions import SerializerValidationError, UnsetPaginationError, NotFoundRequiredParameterError
from django.utils.datastructures import MultiValueDictKeyError
from .response import get_status_by_code


class HeaderMixin:
    def get_auth_user(self, request):
        """
        유저 token을 받아 해당 유저의 id를 return한다.
        """
        token_key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = Token.objects.get(key=token_key)
        return token.user_id


class ValidationMixin:
    """
    views 단에서 validation을 할 수 있는 method들을 구현.
    models 쪽 validation은 serializer에서 검증이 들어가 get_valid_szr을 통해 SerializerValidationError로 raise된다.
    클라이언트 측 오류가 아닌 유저 쪽에서 입력 오류를 낼 수 있는 것들은 models쪽에서 validation하기엔 views쪽에서 구분해주어야 하는 경우가 있다.
    이런 경우, ValidationMixin에서 validation 처리를 해준다.
    """
    def get_valid_szr(self, serializer, data=empty, instance=None, **kwargs):
        """
        models 쪽 validation은 serializer에서 검증이 들어가 get_valid_szr을 통해 SerializerValidationError로 raise된다.
        serializer.is_valid()로 검증을 해주는 부분에 대한 method
        """
        szr = serializer(instance=instance, data=data, **kwargs)

        if szr.is_valid() is False:
            raise SerializerValidationError(f'Not valid serializer {serializer.__name__}', code=get_status_by_code(400), params=szr.errors)
        return szr
    
    def get_query_or_none(self, query, key):
        """
        쿼리스트링에서 해당 키로 불러올 수 있는지 여부를 확인 후, 불러올 수 있는 값 return 아니면 None
        """
        try:
            return query[key]
        except MultiValueDictKeyError:
            return None
    
    def get_query_or_exception(self, query, key):
        """
        쿼리스트링에서 해당 키로 불러올 수 있는지 여부 확인 후, 불러올 수 있는 값 return 아니면 NotFoundRequiredParameterError
        """
        try:
            return query[key]
        except MultiValueDictKeyError:
            raise NotFoundRequiredParameterError(key)
    
    def get_paginate_parameters(self, query):
        limit = self.get_query_or_none(query, 'limit')
        offset = self.get_query_or_none(query, 'offset')
        if limit and offset:
            limit = int(limit)
            offset = int(offset)
            return limit, offset
        else:
            raise UnsetPaginationError


class CoreMixin(
    HeaderMixin, ValidationMixin
):
    pass
