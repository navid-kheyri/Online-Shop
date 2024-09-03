from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Order, OrderItem
from .serializers import OrderItemModelSerializer, OrderModelSerializer
from website.models import Product
from ...cart import Cart
from django.contrib.auth.decorators import login_required
from customers.models import Address
from .serializers import CartAddSerializer, CartRemoveSerializer, AddressSerializer
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderModelSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        order = get_object_or_404(Order,pk=pk)
        serializer = OrderModelSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):

        order=get_object_or_404(Order,pk=pk)
        serializer = OrderModelSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):

        order=get_object_or_404(Order,pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        order_items = OrderItem.objects.all()
        serializer = OrderItemModelSerializer(order_items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderItemModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        order_item = get_object_or_404(OrderItem,pk=pk)
        serializer = OrderItemModelSerializer(order_item)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):

        order_item = get_object_or_404(OrderItem,pk=pk)
        serializer = OrderItemModelSerializer(order_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        
        order_item = get_object_or_404(OrderItem,pk=pk)
        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CartAddSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(
                Product, id=serializer.validated_data['product_id'])
            quantity = serializer.validated_data['quantity']
            cart = Cart(request)
            cart.add(product, quantity)
            return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCartAPIView(APIView):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = []
        for key, item in cart.cart.items():
            product = Product.objects.get(id=key)
            cart_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': item['quantity'],
                'price': product.price,
                'total_price': product.price * item['quantity']
            })
        return Response(cart_items, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CartRemoveSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(
                Product, id=serializer.validated_data['product_id'])
            quantity = serializer.validated_data['quantity']
            cart = Cart(request)
            cart.remove(product, quantity)
            return Response({'message': 'Product removed from cart'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFromCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CartRemoveSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(
                Product, id=serializer.validated_data['product_id'])
            cart = Cart(request)
            cart.deleteitem(product)
            return Response({'message': 'Product deleted from cart'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CartAddSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(
                Product, id=serializer.validated_data['product_id'])
            quantity = serializer.validated_data['quantity']
            cart = Cart(request)
            cart.update(product, quantity)
            return Response({'message': 'Cart updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = []
        for key, item in cart.cart.items():
            product = Product.objects.get(id=key)
            cart_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': item['quantity'],
                'price': product.price,
                'total_price': product.price * item['quantity'],
                # 'image_url': product.images.first().image.url
            })
        return Response({'cart_items': cart_items}, status=status.HTTP_200_OK)


class CheckoutAPIView(LoginRequiredMixin,APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart.cart:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_200_OK)
        cart_items = []
        for key, item in cart.cart.items():
            product = Product.objects.get(id=key)
            #####
            if product.discount:
                price= product.count_discount()
            elif product.percent_discount:
                price= product.count_discount()
            else:
                price= product.price
            cart_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': item['quantity'],
                'price': product.price,
                'total_price': price * item['quantity']
            })
        addresses = Address.objects.filter(user=request.user)
        address_data = AddressSerializer(addresses, many=True).data
        response_data = {
            'user_id': request.user.id,
            'cart_items': cart_items,
            'addresses': address_data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart.cart:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        address_data = request.data.get('address')
        address_id = request.data.get('address_id')

        if address_data:
            address_data['user'] = request.user.id
            address_serializer = AddressSerializer(
                data=address_data, context={'request': request})
            if address_serializer.is_valid():
                address = address_serializer.save()
            else:
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif address_id:
            address = Address.objects.filter(
                id=address_id, user=request.user).first()
            if not address:
                return Response({'message': 'Invalid address ID'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, address=address)

        for key, item in cart.cart.items():
            product = Product.objects.get(id=key)
            if product.discount:
                price = product.count_discount()
                item_total_price = price * item['quantity']
            elif product.percent_discount:
                price= product.count_discount()
                item_total_price = price * item['quantity']
            else:
                item_total_price = product.price * item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                item_total_price=item_total_price
            )

        cart.clear()
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)


class CartCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return JsonResponse({'cart_count': len(cart)})
