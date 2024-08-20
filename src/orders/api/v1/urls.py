from django.urls import path
from .views import (OrderListCreateAPIView, OrderDetailAPIView, OrderItemListCreateAPIView, 
                UpdateCartAPIView,CartCountAPIView,OrderItemDetailAPIView,AddToCartAPIView,RemoveFromCartAPIView,
                CartDetailAPIView,CheckoutAPIView,DeleteFromCartAPIView)


app_name = 'api-v1'

urlpatterns = [
    path('cart/add/', AddToCartAPIView.as_view(), name='cart-add'),
    path('cart/remove/', RemoveFromCartAPIView.as_view(), name='cart-remove'),
    path('delete-from-cart/', DeleteFromCartAPIView.as_view(), name='delete-from-cart'),
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/update/', UpdateCartAPIView.as_view(), name='cart-update'),
    path('cart/checkout/', CheckoutAPIView.as_view(), name='cart_to_order'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('order-items/', OrderItemListCreateAPIView.as_view(), name='order_item_list_create'),
    path('order-items/<int:pk>/', OrderItemDetailAPIView.as_view(), name='order_item_detail'),
    path('cart/count/', CartCountAPIView.as_view(), name='cart-count'),
]
