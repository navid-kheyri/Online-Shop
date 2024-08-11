from django.shortcuts import render
from django.views.generic import CreateView
from .models import Product

# Create your views here.


def index(request):
    return render(request, 'index.html')
