from rest_framework.serializers import ModelSerializer
from funding.apps.user.models import User, Pocket

class AccountCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"]
        )
        return user
