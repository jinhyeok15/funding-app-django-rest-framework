from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User


