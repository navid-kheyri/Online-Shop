from django.urls import path
from .views import CustomerDetailView,OwnerDashboardView

app_name='dashboard'

urlpatterns = [
    path('customer/<pk>/detailes/',CustomerDetailView.as_view(),name='user'),
    path('owner_dashboard/',OwnerDashboardView.as_view(),name='owner-dashboard'),
    
]