from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from .models import Product,Category
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

class IndexListView(ListView):
    template_name='index.html'
    model=Product
    context_object_name='product'

    def get_queryset(self):
        category=Category.objects.all()
        return category

    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['category']=self.get_queryset()
        return context
