from rest_framework.authtoken.models import Token


def authorize(func):
    def wrapper(self, request, *args, **kwargs):
        token_key = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = Token.objects.get(key=token_key)
        return func(self, request, token.user_id, *args, **kwargs)
    return wrapper
