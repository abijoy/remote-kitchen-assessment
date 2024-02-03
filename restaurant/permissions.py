# permissions.py
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import (
    Restaurant,
    Menu,
    Item,
)


class IsRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        res = get_object_or_404(Restaurant, id=view.kwargs['pk'])
        return request.user == res.owner

    def has_object_permission(self, request, view, obj):
        res = get_object_or_404(Restaurant, id=view.kwargs['pk'])
        return request.user == res.owner


class IsRestaurantEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        res = get_object_or_404(Restaurant, id=view.kwargs['pk'])
        is_employee = request.user in res.employees.all()
        if is_employee and request.method in permissions.SAFE_METHODS:
            return True


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class MenuPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        menu = get_object_or_404(Menu, id=view.kwargs['menu_id'])
        res = get_object_or_404(Restaurant, id=view.kwargs['pk'])
        print(menu, res)
        if menu not in res.menus.all():
            return False

        print(res)
        # return False
        if request.user.role == 'employee' and request.method in permissions.SAFE_METHODS:
            return request.user in res.employees.all()
        return request.user == res.owner

    def has_object_permission(self, request, view, obj):
        print('### Menu object permisssion #####')
        menu = get_object_or_404(Menu, id=view.kwargs['menu_id'])
        return request.user == menu.restaurant.owner


class ItemPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        res = get_object_or_404(Restaurant, id=view.kwargs['pk'])
        menu = get_object_or_404(Menu, id=view.kwargs['menu_id'])
        item = get_object_or_404(Item, id=view.kwargs['item_id'])

        print(menu, res)
        print('########')
        print(menu.items.all().values_list('id', 'title'))

        if item not in menu.items.all():
            return False

        print(res)
        # return False
        if request.user.role == 'employee' and request.method in permissions.SAFE_METHODS:
            return request.user in res.employees.all()
        return request.user == res.owner

    def has_object_permission(self, request, view, obj):
        print('### Item object permisssion #####')
        return request.user == obj.menu.restaurant.owner
