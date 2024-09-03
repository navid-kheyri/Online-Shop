from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseForbidden
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Vendor, VendorRating
from orders.models import Order, OrderItem
from website.models import Product
from .forms import ProductDetailModelForm, VendorModelForms, UserModelForm, VendorChangeDetailForm, VendorRatingForm, OrderItemModelForm
from django.utils.decorators import method_decorator
from accounts.decorators import roles_required
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# Create your views here.


@method_decorator(roles_required('manager', 'owner'), name='dispatch')
class AddVendorCreateView(CreateView):
    """
    این کلاس برای ایجاد فروشگاه جدید نوشته شده است.
    """
    model = Vendor
    template_name = 'shop/add-vendor.html'
    form_class = VendorModelForms
    success_url = reverse_lazy("dashboard:owner-dashboard")

    def form_valid(self, form):
        """
        در اینجا هدف این است که یوزری که لاگین کرده به عنوان مدیر 
        بصورت پیش فرض ثبت شود  پس کد به این صورت نوشته میشود
        """
        response = super().form_valid(form)
        self.object.user.set([self.request.user])
        form.save()
        return response


@method_decorator(roles_required('manager', 'owner'), name='dispatch')
class AddEmployeeCreateView(CreateView):
    """
    این کلاس برای ایجاد منیجر و اوپراتور توسط مدیر نوشته شده است.
    """
    model = User
    template_name = 'shop/add-employee.html'
    form_class = UserModelForm
    success_url = reverse_lazy("dashboard:owner-dashboard")

    def get_form_kwargs(self):
        """
        در اینجا ما در واقع  ریکوئست را به فرم پاس میدهیم تا 
        با استفاه از آن فرم به ریکویست دست پیدا کنیم و 
        user type را فیلتر کنیم
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """
        در اینجا هنگام ایجاد کارمند استف را ترو میکنیم
        """
        # form_data = form.cleaned_data
        # category = Categories.objects.create(name=form_data['name'], description=form_data['description'])
        # UserImage.objects.create(category=category, image=form_data['input_image'])
        self.object = form.save(commit=False)
        self.object.is_staff = True
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


method_decorator(
    (roles_required('owner', 'manager', 'operator')), name='dispatch')


class MyVendorDetatilView(LoginRequiredMixin, DetailView):
    """
    برای دیدن آپشن های هر فروشگاه
    """
    model = Vendor
    template_name = 'shop/my-vendors.html'

    def dispatch(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
        if not vendor.user_has_permission(request.user):
            return HttpResponseForbidden("You do not have permission to access this vendor.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.object
        owner = vendor.user.get(user_type='owner')
        context['vendor'] = vendor
        context['owner'] = owner
        return context


@method_decorator(roles_required('manager', 'operator', 'owner'), name='dispatch')
class MyProductsListView(ListView):
    """
    برای دیدن محصولات هر فزوشگاه
    """
    model = Vendor
    template_name = 'shop/my-products.html'

    def dispatch(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
        if not vendor.user_has_permission(request.user):
            return HttpResponseForbidden("You do not have permission to access this vendor.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = Vendor.objects.prefetch_related(
            'vendor_products').filter(pk=self.get_queryset())
        for products in vendor:
            product = products.vendor_products.all()
        context['vendor'] = vendor
        context['product'] = product

        return context


method_decorator((roles_required('owner', 'manager')), name='dispatch')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'shop/dashboard-product-detail.html'
    form_class = ProductDetailModelForm
    success_url = reverse_lazy("dashboard:owner-dashboard")

    def get_queryset(self):
        products = Product.objects.filter(vendor__user=self.request.user)
        return products

    def dispatch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        if not product in self.get_queryset():
            return HttpResponseForbidden("You are not allowed to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        در اینجا ما در واقع  ریکوئست را به فرم پاس میدهیم تا 
        با استفاه از آن فرم به ریکویست دست پیدا کنیم 
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


method_decorator((roles_required('owner', 'manager')), name='dispatch')


class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    template_name = 'shop/vendor-change-detail.html'
    form_class = VendorChangeDetailForm

    def dispatch(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
        if not vendor.user_has_permission(request.user):
            return HttpResponseForbidden("You do not have permission to access this vendor.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('vendors:my-vendor', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


# class AllShopsListView(ListView):
#     model = Vendor
#     template_name = 'shop/all-shops.html'


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class ShopPageDetailView(DetailView):
    model = Vendor
    template_name = 'shop/shop-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = Vendor.objects.get(id=self.object.id)
        user = self.request.user.id

        paid_orders = Order.objects.filter(
            user=user).prefetch_related('order_item__product')
        vendors = []
        for order in paid_orders:
            orderitems = order.order_item.all()
            for item in orderitems:
                shop = item.product.vendor.first().name
                vendors.append(shop)

        rating = VendorRating.objects.filter(vendor=vendor, user=user)
        products = Product.objects.prefetch_related(
            'vendor').filter(vendor=self.object.id)
        context['products'] = products
        context['vendor'] = vendor
        context['my_rating'] = rating
        context['shops'] = set(vendors)
        return context


@method_decorator(roles_required('customer'), name='dispatch')
class VendorRateCreateView(CreateView):
    model = VendorRating
    form_class = VendorRatingForm
    template_name = 'shop/shop-rating.html'

    def get_success_url(self):
        return reverse_lazy('vendors:shop-page', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        rating = form.save(commit=False)
        rating.user = self.request.user
        vendor = Vendor.objects.get(pk=self.kwargs['pk'])
        rating.vendor = vendor
        vendor.rating_count += 1
        vendor.sum_rating += rating.rating
        vendor.update_average_rating()
        vendor.save()
        rating.save()
        return super().form_valid(form)


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class AllShopsListView(ListView):
    model = Vendor
    template_name = 'shop/all-shops.html'
    context_object_name = 'vendors'

    def get_queryset(self):
        filter_type = self.request.GET.get('filter')
        if filter_type == 'most-selling':
            orders = OrderItem.objects.all()
            total_sales = orders.values('product__vendor').annotate(
                total=Sum('quantity')).order_by('-total')
            vendors = []
            for vendor in total_sales:
                vendors.append(Vendor.objects.get(
                    id=vendor['product__vendor']))
            return vendors

        elif filter_type == 'top-rating':
            vendors = Vendor.objects.order_by('-average_rating')
            return vendors

        elif filter_type == 'newest-vendors':
            vendors = Vendor.objects.all().order_by('-created_at')
            return vendors

        return super().get_queryset()


# class MostSellingVendorsListView(ListView):
#     model = Product
#     template_name = 'filters/most-selling-vendors.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         orders = OrderItem.objects.filter(order__is_paid=True)
#         total_sales = orders.values('product__vendor').annotate(
#             total=Sum('quantity')).order_by('-total')
#         shops = []
#         for vendor in total_sales:
#             shops.append(Vendor.objects.get(id=vendor['product__vendor']))
#         context['vendors'] = shops
#         return context


# class TopRatedVendorsListView(ListView):
#     model = Vendor
#     template_name = 'filters/top-rated-vendors.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         vendors = Vendor.objects.order_by('-average_rating')
#         context['vendors'] = vendors
#         return context


# class NewestVendorsListView(ListView):
#     template_name = 'filters/newest-vendors.html'
#     model = Vendor

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         last_vendors = Vendor.objects.all().order_by('-created_at')
#         context['last_vendors'] = last_vendors
#         return context

@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class TopSellingProductShop(DetailView):
    model = Vendor
    template_name = 'filters/top-selling-product-shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderItem.objects.all()
        total_sales = orders.values('product_id').annotate(
            total=Sum('quantity')).order_by('-total')
        products = []
        for product in total_sales:
            product = Product.objects.filter(
                id=product['product_id'], vendor=self.kwargs['pk']).first()
            if product:
                products.append(product)
        context['products'] = products
        return context


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class TopRatedProductShop(DetailView):
    model = Vendor
    template_name = 'filters/top-rated-product-shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(
            vendor=self.kwargs['pk']).order_by('-average_rating')
        context['products'] = products
        return context


@method_decorator(roles_required('customer', 'admin', 'anonymous'), name='dispatch')
class MostExpensiveProductShop(DetailView):
    model = Vendor
    template_name = 'filters/expensive-product-shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(
            vendor=self.kwargs['pk']).order_by('-price')
        context['products'] = products
        return context


@method_decorator(roles_required('manager', 'operator', 'owner'), name='dispatch')
class MyVendorOrders(DetailView):
    model = Vendor
    template_name = 'shop/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_object().vendor_products.prefetch_related('product_item').all()
        orderitems = []
        for product in products:
            for item in product.product_item.filter(status='pending'):
                orderitems.append(item)
        context['orderitems'] = orderitems
        return context


@method_decorator(roles_required('manager', 'operator', 'owner'), name='dispatch')
class VendorOrdersDetailView(UpdateView):
    model = OrderItem
    template_name = 'shop/order-detail.html'
    form_class = OrderItemModelForm
    success_url =reverse_lazy('dashboard:owner-dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs['pk'])
        context['order'] = order
        return context
