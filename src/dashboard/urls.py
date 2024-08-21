from django.urls import path
from .views import (CustomerDetailView,MyVendorListView,CustomerUpdateView,CustomerChangePasswordView,
                    CustomerOrdersListView,CustomerOrderItemDetailView,MyCommentDetailView)

app_name='dashboard'

urlpatterns = [
    path('customer/<pk>/detailes/',CustomerDetailView.as_view(),name='user'),
    path('owner_dashboard/',MyVendorListView.as_view(),name='owner-dashboard'),
    path('customer/<pk>/update/',CustomerUpdateView.as_view(),name='customer-update'),
    path('customer_change_password/',CustomerChangePasswordView.as_view(),name='customer-change-password'),
    path('my_orders/',CustomerOrdersListView.as_view(),name='my-orders'),
    path('order/<pk>/order_items/',CustomerOrderItemDetailView.as_view(),name='order-item'),
    path('customer/<int:pk>/my_comments/',MyCommentDetailView.as_view(),name='my-comment'),
    
]