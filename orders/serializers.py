from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        # fields = ['id', 'items']
        # items = serializers.ListField(
        #     child=serializers.DictField()
        # )

        fields = ['id',
                  'payment_status', 'order_placed_by', 'payment_id']
        read_only_fields = ('id', 'order_placed_by',)
