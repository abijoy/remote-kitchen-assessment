# permissions.py
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from restaurant.models import (
    Restaurant,
    Menu,
    Item,
)


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
        if request.method in permissions.SAFE_METHODS:
            return True
