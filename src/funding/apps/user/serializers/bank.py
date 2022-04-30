from ..models import Pocket
from rest_framework.serializers import ModelSerializer


class PocketSerializer(ModelSerializer):

    class Meta:
        model = Pocket
        fields = '__all__'
