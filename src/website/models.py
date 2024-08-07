from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator)
from django_jalali.db import models as jmodels
from vendors.models import Vendor
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='category/%Y/%m/%d/', blank=True, null=True, default='default.jpg')
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.DO_NOTHING, related_name='sub_categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity_in_stock = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product/%Y/%m/%d/')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="images")

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating = models.IntegerField(default=1, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return self.rating


class Comment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.title
