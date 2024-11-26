from django.db.models.base import Model as Model
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
from django.core.paginator import Paginator

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


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class CategoryProductDetailView(DetailView):
    model = Category
    template_name = 'shop/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        category_product = category.category_products.all()
        paginator = Paginator (category_product, 4)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        # context['category_product'] = category_product
        context['page_obj'] = page_obj
        context['paginator'] = paginator

        return context


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class AllCategoriesListView(ListView):
    """
    برای دیدن دسته بندی ها در صفحه all categories
    """
    model = Category
    template_name = 'website/all-categories.html'
    context_object_name = 'categoriess'
    paginate_by = 6



@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user.id
        paid_orders = Order.objects.filter(
            user=user).prefetch_related('order_item__product') #az jense Order
        product_name = [] # ina baraye rating hast k orderhaye done shode ro baraye current user miare k agar in product to in list bood va rate nadade bodim
        for order in paid_orders:
            orderitems = order.order_item.all()
            for item in orderitems:
                prod = item.product.name
                product_name.append(prod)
        rating = Rating.objects.filter(product=product, user=user)
        comments = product.Product_comments.filter(comment_type='confirmed') #show all confirmed comment of current product
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


@method_decorator(roles_required('customer'), name='dispatch')
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


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class SubCategoriesDetailView(DetailView):
    model = Category
    template_name = 'shop/sub-categories.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['pk'])
        sub_cat = category.sub_categories.all()
        context['sub_cat'] = sub_cat
        return context
    

@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class IndexListView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'
    paginate_by=4


    def get_queryset(self):
        
        filter_type = self.request.GET.get('filter')

        if filter_type == 'top-selling':
            orders = OrderItem.objects.all()
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
        return super().get_queryset() # in by default Product.objects.all() return mikone age nazarim none mide
    

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
            if products.exists(): #True false mide
                context['productss'] = products
            if vendors.exists():
                context['vendorss'] = vendors
            else:
                context["not_found"] = f'"{search}" Does Not Exist.'
        return context
