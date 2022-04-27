from rest_framework.authtoken.models import Token
from funding.apps.core.exceptions import SerializerValidationError


class AuthMixin:
    def get_auth_user(self, request):
        token_key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = Token.objects.get(key=token_key)
        return token.user_id


class ValidationMixin:
    def get_valid_szr(self, serializer, data):
        szr = serializer(data=data)

        if szr.is_valid() is False:
            raise SerializerValidationError(f'Not valid serializer {serializer.__name__}', szr.errors)
        return szr

class IntegrationMixin(
    AuthMixin, ValidationMixin
):
    pass
