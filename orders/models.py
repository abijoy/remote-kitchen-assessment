from django.db import models
from users.models import CustomUser
from restaurant.models import Item
from django.conf import settings
from .mixins import TimestampMixin


PAYMENT_STATUS_CHOICES = [
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
]

# Create your models here.


class Order(TimestampMixin):
    order_placed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    # items = models.ManyToManyField(Item)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_id = models.CharField(unique=True, null=True, blank=True, max_length=200)

    @property
    def subtotal(self):
        sub_total = sum([float(item.price) for item in self.items.all()])
        return sub_total

    @property
    def total(self):
        import math
        # lets impose 7% tax on food
        tax = float(self.subtotal) * (7 / 100)
        return round(self.subtotal + tax, 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordereditems')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)


    def __str__(self):
        return f'Order ID: {self.order.id} - Item: {self.item} - Quantity: {self.quantity}'
