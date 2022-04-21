from rest_framework.authtoken.models import Token


class AuthMixin:
    def get_auth_user(self, request):
        token_key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = Token.objects.get(key=token_key)
        return token.user_id
