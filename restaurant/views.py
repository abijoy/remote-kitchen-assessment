from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .models import Restaurant, Menu, Item
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    ItemSerializer
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import (
    IsOwner,
    IsEmployee,
    MenuPermission,
    ItemPermission,
    IsRestaurantOwner,
    IsRestaurantEmployee,
)


class RestaurantList(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsEmployee]

    def get_queryset(self):
        if self.request.user.role == 'owner':
            return Restaurant.objects.filter(owner=self.request.user)
        if self.request.user.role == 'employee':
            return Restaurant.objects.filter(employees__in=[self.request.user])

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated,
                          IsRestaurantOwner | IsRestaurantEmployee]

    def get_queryset(self):
        if self.request.user.role == 'owner':
            return Restaurant.objects.filter(owner=self.request.user)
        if self.request.user.role == 'employee':
            return Restaurant.objects.filter(employees__in=[self.request.user])

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MenuList(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated,
                          IsRestaurantOwner | IsRestaurantEmployee]

    def get_restaurant(self):
        restaurant_id = self.kwargs['pk']
        res = Restaurant.objects.get(id=restaurant_id)
        return res

    def post(self, request, *args, **kwargs):
        res = self.get_restaurant()
        if request.user != res.owner:
            return Response('Unauthorized request', status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        res = self.get_restaurant()
        # print(res)
        if request.user == res.owner or request.user in res.employees.all():
            return self.list(request, *args, **kwargs)
        return Response('Forbidden request', status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        restaurant_obj = self.get_restaurant()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, restaurant_obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, restaurant_obj):
        serializer.save(restaurant=restaurant_obj)

    def get_queryset(self):
        res = self.get_restaurant()
        if self.request.user.role == 'owner' and self.request.user == res.owner:
            return res.menus.all()
        if self.request.user.role == 'employee':
            if self.request.user in res.employees.all():
                return res.menus.all()

    # def perform_create(self, serializer):
    #     if self.request.user == serializer.restaurant.owner:
    #         serializer.save(owner=self.request.user)


class MenuDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = MenuSerializer
    permission_classes = [
        IsAuthenticated, IsRestaurantOwner | IsRestaurantEmployee, MenuPermission]

    def get_menu(self):
        menu_id = self.kwargs['menu_id']
        return Menu.objects.get(id=menu_id)

    def get_restaurant(self):
        restaurant_id = self.kwargs['pk']
        res = Restaurant.objects.get(id=restaurant_id)
        return res

    def get_object(self):
        obj_id = self.kwargs['menu_id']
        return get_object_or_404(Menu, id=obj_id)

    def get_queryset(self):
        res = self.get_restaurant()
        print(res)
        if self.request.user.role == 'owner' and self.request.user == res.owner:
            # return Menu.objects.get(id=self.kwargs['menu_id'])
            return Menu.objects.filter(restaurant=res)

        if self.request.user.role == 'employee':
            if self.request.user in res.employees.all():
                return Menu.objects.get(id=self.kwargs['menu_id'])

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)


class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [
        IsAuthenticated, IsRestaurantOwner | IsRestaurantEmployee, MenuPermission]

    # def get_restaurant(self):
    #     restaurant_id = self.kwargs['pk']
    #     res = Restaurant.objects.get(id=restaurant_id)
    #     return res

    # def post(self, request, *args, **kwargs):
    #     res = self.get_restaurant()
    #     if request.user != res.owner:
    #          return Response('Unauthorized request', status=status.HTTP_400_BAD_REQUEST)
    #     return self.create(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     print('############# getting list ##########')
    #     try:
    #         res = self.get_restaurant()
    #     except Exception as e:
    #         print(e)
    #     # print(res)
    #     if request.user == res.owner or request.user in res.employees.all():
    #         return self.list(request, *args, **kwargs)
    #     return Response('Forbidden request', status=status.HTTP_403_FORBIDDEN)

    # def create(self, request, *args, **kwargs):
    #     restaurant_obj = self.get_restaurant()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer, restaurant_obj)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer, restaurant_obj):
    #     serializer.save(restaurant=restaurant_obj)

    def get_menu(self):
        menu_id = self.kwargs['menu_id']
        return get_object_or_404(Menu, id=menu_id)

    def get_restaurant(self):
        restaurant_id = self.kwargs['pk']
        res = get_object_or_404(Restaurant, id=restaurant_id)
        return res

    def get_queryset(self):
        res = self.get_restaurant()
        menu = self.get_menu()
        # return Item.objects.filter(menu=menu)
        if self.request.user.role == 'owner' and self.request.user == res.owner:
            print('$$$$$$$$$ Im the owner')
            return menu.items.all()
        if self.request.user.role == 'employee':
            if self.request.user in res.employees.all():
                return menu.items.all()

    # def perform_create(self, serializer):
    #     if self.request.user == serializer.restaurant.owner:
    #         serializer.save(owner=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner |
                          IsRestaurantEmployee, MenuPermission, ItemPermission]

    def get_queryset(self):
        res = get_object_or_404(Restaurant, id=self.kwargs['pk'])
        menu = get_object_or_404(Menu, id=self.kwargs['menu_id'])

        if self.request.user == res.owner:
            return menu.items.all()

        if self.request.user.role == 'employee':
            if self.request.user in res.employees.all():
                return menu.items.all()

    def get_object(self):
        item_id = self.kwargs['item_id']
        return get_object_or_404(Item, id=item_id)
