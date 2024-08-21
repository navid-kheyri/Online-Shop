from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from .models import Product, Category, Comment
from vendors.models import Vendor
from .forms import AddProductModelForm, CommentModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


class AddProductCreateView(CreateView):
    model = Product
    template_name = 'website/add-product.html'
    form_class = AddProductModelForm
    success_url = reverse_lazy('dashboard:owner-dashboard')

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        در اینجا ما در واقع  ریکوئست را به فرم پاس میدهیم تا 
        با استفاه از آن فرم به ریکویست دست پیدا کنیم 
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class IndexListView(ListView):
    template_name = 'index.html'
    model = Product

    # def get_queryset(self):
    #     category=Category.objects.all()
    #     return category

    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context['category']=self.get_queryset()
    #     return context


class CategoryProductDetailView(DetailView):
    model = Category
    template_name = 'shop/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        category_product = category.category_products.all()
        for prod in category_product:
            image = prod.images.all()

        context['category_product'] = category_product
        context['image'] = image

        return context


class AllCategoriesListView(ListView):
    """
    برای دیدن دسته بندی ها در صفحه all categories
    """
    model = Category
    template_name = 'website/all-categories.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        comments = product.Product_comments.all()
        context['comments'] = comments
        context['product'] = product
        context['form'] = CommentModelForm()
        return context

    def post(self, request,*args,**kwargs):
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = self.get_object()
            comment.comment_type='pending'
            comment.save()
            return redirect('website:product-detail', pk=self.get_object().id)
        # ==> age form valid nabood method get DetailView seda zade mishe
        return self.get(request,*args,**kwargs)
