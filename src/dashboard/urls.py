from django.urls import path
from .views import CustomerDetailView,MyVendorListView

app_name='dashboard'

urlpatterns = [
    path('customer/<pk>/detailes/',CustomerDetailView.as_view(),name='user'),
    path('owner_dashboard/',MyVendorListView.as_view(),name='owner-dashboard'),
    # path('my_vendors/',MyVendorListView.as_view(),name='my-vendor'),
    
]