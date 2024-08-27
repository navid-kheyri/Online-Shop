from django.urls import path
from .views import (AddProductCreateView ,IndexListView,CategoryProductDetailView,AllCategoriesListView,ProductDetailView,SubCategoriesDetailView,
                    RatingProductCreateView,TopSellingListView,TopRatedListView,MostaExpensiveListView)

app_name='website'

urlpatterns = [
    path('',IndexListView.as_view(),name='index'),
    path('add_product/',AddProductCreateView.as_view(),name='add-product'),
    path('category/<pk>/',CategoryProductDetailView.as_view(),name='category-product'),
    path('all_categories/',AllCategoriesListView.as_view(),name='all-categories'),
    path('product_detail/<pk>/',ProductDetailView.as_view(),name='product-detail'),
    path('sub-categories/<pk>/',SubCategoriesDetailView.as_view(),name='sub-categories'),
    path('product/<pk>/rating-product/',RatingProductCreateView.as_view(),name='rating-product'),
    path('top_selling/',TopSellingListView.as_view(),name='top-selling'),
    path('top_rated/',TopRatedListView.as_view(),name='top-rated'),
    path('most_expensive/',MostaExpensiveListView.as_view(),name='most-expensive'),
    
]