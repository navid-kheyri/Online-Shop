from django.contrib import admin
from .models import Cart, OrderItem
# Register your models here.


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['status', 'crated_at', 'total_price']
    ordering = ['status']

    def total_price(self, instance):
        return instance.get_total_amount()
