from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError


class AuthMixin:
    def get_auth_user(self, request):
        token_key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = Token.objects.get(key=token_key)
        return token.user_id


class ValidationMixin:
    def get_valid_szr(self, serializer, data):
        szr = serializer(data=data)

        if szr.is_valid() is False:
            raise ValidationError(f'Not valid serializer {serializer.__name__}')
        return szr

class IntegrationMixin(
    AuthMixin, ValidationMixin
):
    pass
