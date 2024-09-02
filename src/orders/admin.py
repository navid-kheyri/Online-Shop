from django.contrib import admin
from .models import OrderItem, Order
# Register your models here.


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['user_item','status', 'product', 'quantity', 'item_total_price']

    def user_item(self, instance):
        return instance.order.user.email


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_at', 'updated_at']
