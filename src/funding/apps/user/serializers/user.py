from rest_framework.serializers import ModelSerializer
from funding.apps.user.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email'
        ]
