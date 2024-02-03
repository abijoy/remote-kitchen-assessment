from django.db import models
from .mixins import TimestampMixin
from django.conf import settings


class Restaurant(TimestampMixin):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='works_at')

    def __str__(self):
        return f'{self.name}'
    

class Menu(TimestampMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    location = models.CharField(max_length=200, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.id } - {self.title} - {self.restaurant}'


class Item(TimestampMixin):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.title} - {self.menu}'
