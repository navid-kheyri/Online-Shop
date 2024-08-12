from django.urls import path
from .views import AddProductCreateView , index,IndexListView

app_name='website'

urlpatterns = [
    path('',IndexListView.as_view(),name='index'),
    path('add_product/',AddProductCreateView.as_view(),name='add-product'),
]