from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from .models import Product, Category, Comment, Rating
from vendors.models import Vendor
from orders.models import Order, OrderItem
from .forms import AddProductModelForm, CommentModelForm, RatingProductModelForm
from django.utils.decorators import method_decorator
from accounts.decorators import roles_required
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


@method_decorator(roles_required('manager', 'owner'), name='dispatch')
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


# @method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
# class IndexListView(ListView):
#     template_name = 'index.html'
#     model = Product

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         last_products = Product.objects.all().order_by('-created_at')[:4]
#         context['last_products'] = last_products
#         return context


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class CategoryProductDetailView(DetailView):
    model = Category
    template_name = 'shop/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        category_product = category.category_products.all()
        context['category_product'] = category_product

        return context


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class AllCategoriesListView(ListView):
    """
    برای دیدن دسته بندی ها در صفحه all categories
    """
    model = Category
    template_name = 'website/all-categories.html'


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user.id
        paid_orders = Order.objects.filter(
            user=user, is_paid=True).prefetch_related('order_item__product')
        product_name = []
        for order in paid_orders:
            orderitems = order.order_item.all()
            for item in orderitems:
                prod = item.product.name
                product_name.append(prod)
        rating = Rating.objects.filter(product=product, user=user)
        comments = product.Product_comments.filter(comment_type='confirmed')
        context['comments'] = comments
        context['product'] = product
        context['form'] = CommentModelForm()
        context['orderitems'] = set(product_name)
        context['my_rating'] = rating
        return context

    def post(self, request, *args, **kwargs):
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = self.get_object()
            comment.comment_type = 'pending'
            comment.save()
            return redirect('website:product-detail', pk=self.get_object().id)
        # ==> age form valid nabood method get DetailView seda zade mishe
        return self.get(request, *args, **kwargs)


class RatingProductCreateView(CreateView):
    model = Rating
    template_name = 'website/rating-product.html'
    form_class = RatingProductModelForm

    def get_success_url(self):
        return reverse_lazy('website:product-detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        rating = form.save(commit=False)
        rating.user = self.request.user
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        rating.product = product
        product.rating_count += 1
        product.sum_rating += rating.rating
        product.update_average_rating()
        product.save()
        rating.save()
        return super().form_valid(form)


class SubCategoriesDetailView(DetailView):
    model = Category
    template_name = 'shop/sub-categories.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        print(pk)
        return pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.get_object())
        sub_cat = category.sub_categories.all()
        context['sub_cat'] = sub_cat
        print(sub_cat)
        return context


# class TopSellingListView(ListView):
#     model = Product
#     template_name = 'filters/top-selling-mainpage.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         orders = OrderItem.objects.filter(order__is_paid=True)
#         total_sales = orders.values('product_id').annotate(
#             total=Sum('quantity')).order_by('-total')
#         products = []
#         for product in total_sales:
#             products.append(Product.objects.get(id=product['product_id']))
#         context['products'] = products
#         return context


# class TopRatedListView(ListView):
#     model = Product
#     template_name = 'filters/top-rated-mainpage.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         products = Product.objects.order_by('-average_rating')
#         context['products'] = products
#         return context


# class MostExpensiveListView(ListView):
#     model = Product
#     template_name = 'filters/most-expensive-mainpage.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         products = Product.objects.order_by('-price')
#         context['products'] = products
#         return context
    

@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class IndexListView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        
        filter_type = self.request.GET.get('filter')

        if filter_type == 'top-selling':
            orders = OrderItem.objects.filter(order__is_paid=True)
            total_sales = orders.values('product_id').annotate(
                total=Sum('quantity')).order_by('-total')
            products = []
            for product in total_sales:
                products.append(Product.objects.get(id=product['product_id']))
            return products
        
        elif filter_type == 'top-rated':
            products = Product.objects.order_by('-average_rating')
            return products
        
        elif filter_type == 'most-expensive':
            products = Product.objects.order_by('-price')
            return products
        return super().get_queryset()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_products = Product.objects.all().order_by('-created_at')[:4]
        context['last_products'] = last_products
        return context
    
    
class SearchListView(ListView):
    model = Product
    template_name ='website/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q' , None).capitalize()
        if search:
            products = Product.objects.filter(name__icontains=search)
            vendors = Vendor.objects.filter(name__icontains=search)
            if products.exists():
                context['productss'] = products
            if vendors.exists():
                context['vendorss'] = vendors
            else:
                context["not_found"] = f'"{search}" Does Not Exist.'
        return context
