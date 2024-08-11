from django.urls import path
from .views import AddVendorCreateView,AddEmployeeCreateView,MyVendorDetatilView

app_name='vendors'

urlpatterns = [
    path('create_vendor/',AddVendorCreateView.as_view(),name='create-vendor'),
    path('add_employee/',AddEmployeeCreateView.as_view(),name='add-employee'),
    path('my_vendors/<pk>/',MyVendorDetatilView.as_view(),name='my-vendor'),
]