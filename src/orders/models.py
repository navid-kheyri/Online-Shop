from django.db import models
from django_jalali.db import models as jmodels
from website.models import Product
from django.contrib.auth import get_user_model
from customers.models import Address

User = get_user_model()

# Create your models here.


class OrderItem(models.Model):
    ORDER_ITEM_STATUS = (
        ('pending', 'pending'),
        ('shipped', 'Shipped')
    )
    quantity = models.PositiveIntegerField()
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="product_item")
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='order_item')
    status = models.CharField(
        max_length=10, choices=ORDER_ITEM_STATUS, default='pending')

    def __str__(self):
        return self.order.user.email


class Order(models.Model):
    ORDER_TYPE = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped')
    )
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=ORDER_TYPE, default='processing')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order')
    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, related_name='order_address')

    def __str__(self):
        return self.user.email
