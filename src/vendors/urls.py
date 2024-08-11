from django.urls import path
from .views import AddVendorCreateView,AddEmployeeCreateView    

app_name='vendors'

urlpatterns = [
    path('create_vendor/',AddVendorCreateView.as_view(),name='create-vendor'),
    path('add_employee/',AddEmployeeCreateView.as_view(),name='add-employee'),
]