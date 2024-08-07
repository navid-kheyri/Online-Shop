from django.urls import path
from .views import CreateVendor

app_name='vendors'

urlpatterns = [
    path('create_vendor/',CreateVendor.as_view(),name='create_vendor')
]