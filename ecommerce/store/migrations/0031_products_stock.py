# Generated by Django 4.1.2 on 2022-12-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
