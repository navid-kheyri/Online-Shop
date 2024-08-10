from django.urls import path
from .views import CreateVendor,VendorCreateView,AddEmployeeCreateView

app_name='vendors'

urlpatterns = [
    # path('create_vendor/',CreateVendor.as_view(),name='create_vendor'),
    path('create_vendor/',VendorCreateView.as_view(),name='create_vendor'),
    path('add_employee/',AddEmployeeCreateView.as_view(),name='add-employee'),
]