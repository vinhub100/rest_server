from rest_framework.permissions import BasePermission
from rest_server.authorization.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


class PlayerRoleOnly(BasePermission):
    def has_permission(self, request, view):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist or Exception:
            return False
        if profile.role == "Player":
            return True
        return False


