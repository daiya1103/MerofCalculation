# Generated by Django 4.0.6 on 2022-07-26 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_remove_seller_sales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='key',
            field=models.CharField(max_length=8, verbose_name='キー'),
        ),
    ]
