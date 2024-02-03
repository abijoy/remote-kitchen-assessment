# Generated by Django 4.2 on 2024-01-25 16:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0002_restaurant_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='works_at', to=settings.AUTH_USER_MODEL),
        ),
    ]