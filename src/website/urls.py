from django.urls import path
from .views import AddProductCreateView ,IndexListView,CategoryProductDetailView,AllCategoriesListView,ProductDetailView

app_name='website'

urlpatterns = [
    path('',IndexListView.as_view(),name='index'),
    path('add_product/',AddProductCreateView.as_view(),name='add-product'),
    path('category/<pk>/',CategoryProductDetailView.as_view(),name='category-product'),
    path('all_categories/',AllCategoriesListView.as_view(),name='all-categories'),
    path('product_detail/<pk>/',ProductDetailView.as_view(),name='product-detail')
]