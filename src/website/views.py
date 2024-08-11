from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Product
from vendors.models import Vendor
from .forms import AddProductModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


class AddProductCreateView(CreateView):
    model=Product
    template_name='website/add-product.html'
    form_class=AddProductModelForm
    success_url=reverse_lazy('dashboard:owner-dashboard')

   


def index(request):
    return render (request,'index.html')
