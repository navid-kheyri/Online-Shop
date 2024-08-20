from django.urls import path , include
from .views import CartDetailView,NewAddressCreateView

app_name='orders'

urlpatterns = [
    path('api/v1/', include('orders.api.v1.urls')),
    path('cart/',CartDetailView.as_view(),name='cart-detail'),
    path('new_address/',NewAddressCreateView.as_view(),name='new-address')
]