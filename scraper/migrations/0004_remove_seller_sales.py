# Generated by Django 4.0.6 on 2022-07-26 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_product_key_product_product_price_seller_sales'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='sales',
        ),
    ]