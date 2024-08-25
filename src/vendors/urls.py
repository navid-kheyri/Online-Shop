from django.urls import path
from .views import (AddVendorCreateView,AddEmployeeCreateView,MyVendorDetatilView,
                    MyProductsListView,ProductUpdateView,VendorUpdateView,AllShopsListView,ShopPageDetailView)

app_name='vendors'

urlpatterns = [
    path('create_vendor/',AddVendorCreateView.as_view(),name='create-vendor'),
    path('add_employee/',AddEmployeeCreateView.as_view(),name='add-employee'),
    path('my_vendors/<pk>/',MyVendorDetatilView.as_view(),name='my-vendor'),
    path('my_vendors/<pk>/my_products/',MyProductsListView.as_view(),name='my-products'),
    path('update_product/<pk>/',ProductUpdateView.as_view(),name='update-product'),
    path('vendor/<pk>/update/',VendorUpdateView.as_view(),name='update-vendor'),
    path('shops/',AllShopsListView.as_view(),name='shops'),
    path('shop_page/<pk>/',ShopPageDetailView.as_view(),name='shop-page'),

]