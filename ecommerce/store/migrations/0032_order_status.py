# Generated by Django 4.1.2 on 2022-12-13 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_products_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True),
        ),
    ]