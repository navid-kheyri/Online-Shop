from django.db import models
from website.models import Product

# Create your models here.


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    item_total_price = models.DecimalField(decimal_places=2)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="order")
    cart = models.ForeignKey(
        'Cart', on_delete=models.DO_NOTHING, related_name='order')

    def total_price(self):
        total = self.product.price * self.quantity
        self.item_total_price = total
        return self.item_total_price

    # TODO discount here or in cart?
