from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import AccountCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class AccountCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = AccountCreateSerializer
