from django.urls import path
from .views import (AddProductCreateView ,IndexListView,CategoryProductDetailView,AllCategoriesListView,ProductDetailView,SubCategoriesDetailView,
                    RatingProductCreateView,SearchListView)  #TopSellingListView,TopRatedListView,MostExpensiveListView,

app_name='website'

urlpatterns = [
    path('',IndexListView.as_view(),name='index'),
    path('add_product/',AddProductCreateView.as_view(),name='add-product'),
    path('category/<pk>/',CategoryProductDetailView.as_view(),name='category-product'),
    path('all_categories/',AllCategoriesListView.as_view(),name='all-categories'),
    path('product_detail/<pk>/',ProductDetailView.as_view(),name='product-detail'),
    path('sub-categories/<pk>/',SubCategoriesDetailView.as_view(),name='sub-categories'),
    path('product/<pk>/rating_product/',RatingProductCreateView.as_view(),name='rating-product'),
    # path('top_selling/',TopSellingListView.as_view(),name='top-selling'),
    # path('top_rated/',TopRatedListView.as_view(),name='top-rated'),
    # path('most_expensive/',MostExpensiveListView.as_view(),name='most-expensive'),
    path('search/',SearchListView.as_view(),name='search')
    
]