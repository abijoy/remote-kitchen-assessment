# Generated by Django 4.2 on 2024-02-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='checkout_session',
            field=models.CharField(max_length=200, null=True),
        ),
    ]