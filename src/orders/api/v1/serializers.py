from rest_framework import serializers
from ...models import Order, OrderItem
from customers.models import Address


class OrderItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderModelSerializer(serializers.ModelSerializer):
    order_item = OrderItemModelSerializer(many=True, read_only=True) #var bayad ba related_name yeki bashe

    class Meta:
        model = Order
        fields = ['id','created_at','updated_at','status','user','address','order_item']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)


class CartRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
