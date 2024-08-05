from django.db import models
from django_jalali.db import models as jmodels
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


class Cart(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        PAID = 'PD', 'Paid'

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.ACTIVE)
    # user = models.ForeignKey(
    # 'accounts.User', on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return self.pk

    def get_total_amount(self):
        total = sum(item.product.price *
                    item.quantity for item in self.order.all())

        return total
