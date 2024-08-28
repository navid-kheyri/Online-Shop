from django.db import models
from django.shortcuts import get_object_or_404
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
    discount = models.DecimalField(default=0,
        max_digits=10, decimal_places=0, blank=True, null=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    rating_count = models.IntegerField(default=0)
    sum_rating = models.IntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=1.00,validators=[
                                            MinValueValidator(1.0), 
                                            MaxValueValidator(5.0)
                                        ])
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="category_products")
    vendor = models.ManyToManyField(
        Vendor, related_name='vendor_products')

    def __str__(self):
        return self.name
    
    def update_average_rating(self):
        if self.rating_count > 0:
            self.average_rating = round(self.sum_rating / self.rating_count, 1)
    
    def count_comments(self):
        return Comment.objects.filter(product=self,comment_type='confirmed').count()
    
    def count_discount(self):
        if self.discount <= self.price:
            final_price= self.price - self.discount
            return final_price
        else :
            raise ValueError("Invalid discount: discount cannot exceed the price")
        
class ProductImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d/',default='default.jpg')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.image.url


class Rating(models.Model):
    rating = models.IntegerField(default=1, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_ratings')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_ratings')

    def __str__(self):
        return str(self.rating)


class Comment(models.Model):
    COMMENT_TYPES = (
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_comments')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='Product_comments')
    comment_type = models.CharField(
        max_length=10, choices=COMMENT_TYPES, default='pending')

    def __str__(self):
        return self.title
