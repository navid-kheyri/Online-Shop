from django.urls import path
from .views import (AddVendorCreateView, AddEmployeeCreateView, MyVendorDetatilView,MyProductsListView, ProductUpdateView, VendorUpdateView, MostExpensiveProductShop,
                    AllShopsListView, ShopPageDetailView, VendorRateCreateView,TopSellingProductShop,TopRatedProductShop,
                    MyVendorOrders,VendorOrdersDetailView) #MostSellingVendorsListView,TopRatedVendorsListView,NewestVendorsListView

app_name = 'vendors'

urlpatterns = [
    path('create_vendor/', AddVendorCreateView.as_view(), name='create-vendor'),
    path('add_employee/', AddEmployeeCreateView.as_view(), name='add-employee'),
    path('my_vendors/<pk>/', MyVendorDetatilView.as_view(), name='my-vendor'),
    path('my_vendors/<pk>/my_products/', MyProductsListView.as_view(), name='my-products'),
    path('update_product/<pk>/', ProductUpdateView.as_view(), name='update-product'),
    path('vendor/<pk>/update/', VendorUpdateView.as_view(), name='update-vendor'),
    path('shops/', AllShopsListView.as_view(), name='shops'),
    path('shop_page/<pk>/', ShopPageDetailView.as_view(), name='shop-page'),
    path('<pk>/rating/', VendorRateCreateView.as_view(), name='shop-rating'),
    path('<pk>/orders/',MyVendorOrders.as_view(),name='orders'),
    path('<pk>/orders_detail/',VendorOrdersDetailView.as_view(),name='order-detail'),
    # path('most_selling/', MostSellingVendorsListView.as_view(), name='most-selling'),
    # path('most_rating/', TopRatedVendorsListView.as_view(), name='most-rating'),
    # path('newest_vendors/', NewestVendorsListView.as_view(), name='newest-vendors'),
    path('top_selling_product_shop/<pk>/', TopSellingProductShop.as_view(), name='top-selling-p-shop'),
    path('top_rating_product_shop/<pk>/', TopRatedProductShop.as_view(), name='top-rating-p-shop'),
    path('expensive_product_shop/<pk>/', MostExpensiveProductShop.as_view(), name='expensie-p-shop'),

]
