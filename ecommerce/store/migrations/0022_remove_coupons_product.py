# Generated by Django 4.1.2 on 2022-12-05 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_products_quantity_products_trending_coupons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupons',
            name='product',
        ),
    ]