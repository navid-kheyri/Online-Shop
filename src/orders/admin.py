from django.contrib import admin
from .models import OrderItem, Order
# Register your models here.


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order_number','buyer','status', 'product', 'quantity', 'item_total_price']

    def buyer(self, instance):
        return instance.order.user.email
    
    def order_number(sellf,instance):
        return instance.order.pk



@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['order_number','user', 'status', 'created_at', 'updated_at']

    def order_number(sellf,instance):
        return instance.pk
