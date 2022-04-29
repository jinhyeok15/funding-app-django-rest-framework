from rest_framework.authtoken.models import Token
from funding.apps.core.exceptions import SerializerValidationError


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
    def get_valid_szr(self, serializer, data):
        """
        models 쪽 validation은 serializer에서 검증이 들어가 get_valid_szr을 통해 SerializerValidationError로 raise된다.
        serializer.is_valid()로 검증을 해주는 부분에 대한 method
        """
        szr = serializer(data=data)

        if szr.is_valid() is False:
            raise SerializerValidationError(f'Not valid serializer {serializer.__name__}', szr.errors)
        return szr

class IntegrationMixin(
    HeaderMixin, ValidationMixin
):
    pass
