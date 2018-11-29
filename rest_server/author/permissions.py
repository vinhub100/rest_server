from rest_framework.permissions import BasePermission
from rest_server.authorization.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


class QuestionAuthorPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return False
        if profile.role == "Player":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author:
            if request.user == obj.author:
                return True
            else:
                return False
        return True

