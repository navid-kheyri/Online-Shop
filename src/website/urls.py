from django.urls import path
from .views import AddProductCreateView , index

app_name='website'

urlpatterns = [
    path('',index,name='index'),
    path('add_product/',AddProductCreateView.as_view(),name='add-product'),
]