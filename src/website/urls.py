from django.urls import path
from .views import AddProductCreateView ,IndexListView,CategoryDetailView,AllCategoriesListView

app_name='website'

urlpatterns = [
    path('',IndexListView.as_view(),name='index'),
    path('add_product/',AddProductCreateView.as_view(),name='add-product'),
    path('category/<pk>/',CategoryDetailView.as_view(),name='category-product'),
    path('all_categories/',AllCategoriesListView.as_view(),name='all-categories'),
]