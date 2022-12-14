# Generated by Django 4.1.2 on 2022-12-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_products_color_variant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='color_variant',
            field=models.ManyToManyField(blank=True, to='store.colorvariant'),
        ),
        migrations.AlterField(
            model_name='products',
            name='size_variant',
            field=models.ManyToManyField(blank=True, to='store.sizevariant'),
        ),
    ]
