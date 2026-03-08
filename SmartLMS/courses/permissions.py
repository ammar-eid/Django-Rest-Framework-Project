from rest_framework import permissions
from .models import Enrollment


class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user


class IsEnrolled(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Enrollment.objects.filter(user=request.user,course=obj.course).exists()