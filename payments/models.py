from django.db import models
from orders.models import Order


PAYMENT_STATUS_CHOICES = [
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
]


class Payment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, related_name='payments')
    checkout_session_id = models.CharField(max_length=200, null=True)
    stripe_payment_intent_id = models.CharField(max_length=200, null=True)
    payer_email = models.EmailField(null=True)
    payer_name = models.CharField(max_length=100, null=True, blank=True)
    payer_phone = models.CharField(max_length=14, null=True, blank=True)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    amount = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
