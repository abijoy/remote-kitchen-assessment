from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwner, IsEmployee
from .serializers import OrderSerializer

from .models import Order, OrderItem
from restaurant.models import Item, Restaurant

import json

# Create your views here.


class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsEmployee]

    def get_queryset(self):
        if self.request.user.role == 'owner':
            return Order.objects.filter(order_placed_by=self.request.user)
        if self.request.user.role == 'employee':
            return Order.objects.filter(order_placed_by=self.request.user)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        # data = request.data.get('items')

        items_with_quantity = data['items']


        item_objects_quantity = [(Item.objects.get(id=iq['item']), iq['quantity'])
                        for iq in items_with_quantity]
        

        print(item_objects_quantity)
        # for iq in items_with_quantity:


        for item in item_objects_quantity:
            res = item[0].menu.restaurant
            print(res)
            print(res.owner)
            if res.owner != request.user and request.user not in res.employees.all():
                return Response("Please select item only from your restaurant's menu", status=400)
            print(res)
            print()
            
        
        # serializer = OrderSerializer(data=request.data)
        # print(serializer.is_valid())
        # if serializer.is_valid():
        order_obj = Order.objects.create(order_placed_by=self.request.user)

        # Now create OrderItem objects based on item_objects
        for item in item_objects_quantity:
            try:
                order_item = OrderItem.objects.create(
                    order=order_obj,
                    item=item[0],
                    quantity=item[1]
                )
                order_item.save()

            except Exception as e:
                print(e)
                return Response('something went wrong!', status=400)

        response_data = {
            'order_id': order_obj.id,
            'items':  items_with_quantity
        }
        return Response(response_data, status=201)
    # return Response('error!', status=400)

    # def perform_create(self, serializer):
    #     serializer.save(order_placed_by=self.request.user)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsEmployee]

    
    def get_queryset(self):
        return Order.objects.filter(order_placed_by=self.request.user)
    

    def get(self, request, *args, **kwargs):
        try:
            order_obj = Order.objects.get(id=kwargs['pk'])
        except Order.DoesNotExist as e:
            print(e)
            return Response('Order ID does not exist', status=404)
        response_data = {
            'id': order_obj.id,
            'items': [ {'item': ordered_item.item.id, 'quantity': ordered_item.quantity} for ordered_item in order_obj.ordereditems.all() ],
            'payment_status': order_obj.payment_status,
            'payment_id': order_obj.payment_id
        }
        return Response(response_data, status=200)
        # return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(order_placed_by=self.request.user)
