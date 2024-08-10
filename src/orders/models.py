from django.db import models
from django_jalali.db import models as jmodels
from website.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="product_item")
    cart = models.ForeignKey(
        'Cart', on_delete=models.DO_NOTHING, related_name='cart_item')
    order = models.ForeignKey(
        'Order', on_delete=models.DO_NOTHING, related_name='order_item')

    def total_price(self):
        total = self.product.price * self.quantity
        self.item_total_price = total
        return self.item_total_price

    # TODO discount here or in cart?


class Cart(models.Model):

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return self.pk

    def get_total_amount(self):
        total = sum(item.product.price *
                    item.quantity for item in self.product_item.all())

        return total


class Order(models.Model):
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = models.jDateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order')
    
    def __str__(self):
        return self.pk
    
    def get_total_amount(self):
        total = sum(item.product.price *
                    item.quantity for item in self.product_item.all())
        return total
    

    #TODO
    def get_address(self):
        pass
