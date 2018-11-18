from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SignUpSerializer, UserRoleSerializer
from .models import UserProfile
# Create your views here.


class SignUp(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class GetRole(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,  request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        role_serializer = UserRoleSerializer(user_profile)
        return Response(role_serializer.data, status=status.HTTP_200_OK)

