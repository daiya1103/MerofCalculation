from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model

class Product(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    keyword = models.CharField(
        verbose_name='キーワード',
        max_length=50
    )

    category = models.CharField(
        verbose_name='カテゴリー',
        max_length=10,
        blank=True,
        null=True
    )

    tag1 = models.CharField(
        verbose_name='サブカテゴリ',
        max_length=10,
        blank=True,
        null=True
    )

    category = models.CharField(
        verbose_name='サブサブカテゴリ',
        max_length=10,
        blank=True,
        null=True
    )

    product_url = models.URLField(
        verbose_name='商品URL',
    )

    product_img = models.URLField(
        verbose_name='商品画像URL'
    )

    product_name = models.CharField(
        verbose_name='商品名',
        max_length=50,
    )

    sold_time = models.CharField(
        verbose_name='売り切れ時間',
        max_length=5,
    )

    seller_name = models.CharField(
        verbose_name='セラー名',
        max_length=50,
    )

    seller_url = models.URLField(
        verbose_name='セラーURL',
    )

    def __str__(self):
        return self.product_name

class Seller(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    seller_name = models.CharField(
        verbose_name='セラー名',
        max_length=50,
    )

    seller_url = models.URLField(
        verbose_name='セラーURL',
    )

    follow = models.BooleanField(
        verbose_name='お気に入り',
        default=False,
    )

class SellerProduct(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    product_img = models.URLField(
        verbose_name='商品画像URL'
    )

    product_name = models.CharField(
        verbose_name='商品名',
        max_length=50,
    )

    today_sold = models.PositiveIntegerField(
        verbose_name='今日の販売個数'
    )

    tomorrow_sold = models.PositiveIntegerField(
        verbose_name='昨日の販売個数'
    )

    d2_sold = models.PositiveIntegerField(
        verbose_name='2日前の販売個数'
    )

    d3_sold = models.PositiveIntegerField(
        verbose_name='3日前の販売個数'
    )