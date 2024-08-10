from django.contrib import admin
from .models import Cart, OrderItem,Order
# Register your models here.


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'total_price']
    ordering = ['created_at']

    def total_price(self, instance):
        return instance.get_total_amount()


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display=['number','cart','product','quantity','item_total_price']

    def number(self,instance):
        return instance.id
    
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=['user','is_paid','created_at','updated_at']