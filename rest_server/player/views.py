from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import permissions
from .permissions import PlayerRoleOnly
from .models import PlayerScore


class Quiz(APIView):
    permission_classes = [permissions.IsAuthenticated, PlayerRoleOnly]

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class GetScore(APIView):
    permission_classes = [permissions.IsAuthenticated, PlayerRoleOnly]

    def get(self, request, *args, **kwargs):
        score_obj = get_object_or_404(PlayerScore, user=request.user)
        data = {'score': score_obj.score}
        return Response(data=data, status=status.HTTP_200_OK)
