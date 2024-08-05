from django.contrib import admin
from .models import Cart, OrderItem
# Register your models here.


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['status', 'created_at', 'total_price']
    ordering = ['status','created_at']

    def total_price(self, instance):
        return instance.get_total_amount()


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display=['number','cart','product','quantity','item_total_price']

    def number(self,instance):
        return instance.id