from rest_framework import permissions
from django.contrib.auth.models import Group


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow User of an Person to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the User of a Person
        return request.user.is_staff or obj.user == request.user


class IsInOrgOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or \
            Group.objects.get(name=obj.name) in request.user.groups.all()
