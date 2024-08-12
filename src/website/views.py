from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView
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

    # def get_queryset(self):
    #     category=Category.objects.all()
    #     return category

    
    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context['category']=self.get_queryset()
    #     return context

class CategoryDetailView(DetailView):
    model=Category
    template_name='shop/category.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        category=self.object
        category_product=category.category_products.all()
        for prod in category_product:
            image=prod.images.all()
        
        context['category_product']=category_product
        context['image']=image
        
        return context
    
class AllCategoriesListView(ListView):
    """
    برای دیدن دسته بندی ها در صفحه all categories
    """
    model=Category
    template_name='website/all-categories.html'