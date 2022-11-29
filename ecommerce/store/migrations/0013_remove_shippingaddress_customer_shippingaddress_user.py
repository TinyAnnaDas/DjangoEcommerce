# Generated by Django 4.1.2 on 2022-11-14 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_remove_order_customer_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='customer',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
