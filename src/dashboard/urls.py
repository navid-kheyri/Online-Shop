from django.urls import path
from .views import CustomerDetailView
app_name='dashboard'

urlpatterns = [
    path('customer/<pk>/detailes/',CustomerDetailView.as_view(),name='user')
]