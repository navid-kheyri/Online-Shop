from django.http import HttpRequest, HttpResponseForbidden
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,UpdateView
from .models import Vendor
from website.models import Product
from .forms import ProductDetailModelForm, VendorModelForms,UserModelForm,VendorChangeDetailForm
from django.utils.decorators import method_decorator
from accounts.decorators import roles_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# Create your views here.


@method_decorator( roles_required('manager','owner') , name='dispatch')
class AddVendorCreateView(CreateView):
    """
    این کلاس برای ایجاد فروشگاه جدید نوشته شده است.
    """
    model=Vendor
    template_name='shop/add-vendor.html'
    form_class=VendorModelForms
    success_url=reverse_lazy("dashboard:owner-dashboard")

    def form_valid(self,form):
        """
        در اینجا هدف این است که یوزری که لاگین کرده به عنوان مدیر 
        بصورت پیش فرض ثبت شود  پس کد به این صورت نوشته میشود
        """
        response = super().form_valid(form)
        self.object.user.set([self.request.user])
        form.save()
        return response

@method_decorator( roles_required('manager','owner') , name='dispatch')
class AddEmployeeCreateView(CreateView):
    """
    این کلاس برای ایجاد منیجر و اوپراتور توسط مدیر نوشته شده است.
    """
    model=User
    template_name='shop/add-employee.html'
    form_class=UserModelForm
    success_url=reverse_lazy("dashboard:owner-dashboard")

    def get_form_kwargs(self):
        """
        در اینجا ما در واقع  ریکوئست را به فرم پاس میدهیم تا 
        با استفاه از آن فرم به ریکویست دست پیدا کنیم و 
        user type را فیلتر کنیم
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self,form):
        """
        در اینجا هنگام ایجاد کارمند استف را ترو میکنیم
        """
        # form_data = form.cleaned_data
        # category = Categories.objects.create(name=form_data['name'], description=form_data['description'])
        # UserImage.objects.create(category=category, image=form_data['input_image'])
        self.object=form.save(commit=False)
        self.object.is_staff=True
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    
method_decorator((roles_required('owner','manager','operator')),name='dispatch')
class MyVendorDetatilView(LoginRequiredMixin,DetailView):
    """
    برای دیدن آپشن های هر فروشگاه
    """
    model = Vendor
    template_name='shop/my-vendors.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor=self.object
        owner=vendor.user.get(user_type='owner')
        context['vendor']=vendor
        context['owner']=owner
        return context
    
@method_decorator( roles_required('manager','operator','owner') , name='dispatch')   
class MyProductsListView(ListView):
    """
    برای دیدن محصولات هر فزوشگاه
    """
    model=Vendor
    template_name='shop/my-products.html'

    def get_queryset(self):
        pk=self.kwargs['pk']
        return pk
    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        vendor=Vendor.objects.prefetch_related('vendor_products').filter(pk=self.get_queryset())
        for products in vendor:
            product=products.vendor_products.all()
        context['vendor']=vendor
        context['product']=product
        
        return context


class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model=Product
    template_name='shop/dashboard-product-detail.html'
    # fields=['name','quantity_in_stock','description','price','discount','average_rating','category']
    form_class=ProductDetailModelForm
    success_url=reverse_lazy("dashboard:owner-dashboard")

    # def dispatch(self, request, *args, **kwargs) :
    #     if int(kwargs.get('pk')) != self.request.user.pk:
    #         return self.handle_no_permission()
    #     if not (request.user.is_manager or request.user.is_owner):
    #         return HttpResponseForbidden("You are not allowed to access this page.")
    #     return super().dispatch(request, *args, **kwargs)


    def get_form_kwargs(self):
        """
        در اینجا ما در واقع  ریکوئست را به فرم پاس میدهیم تا 
        با استفاه از آن فرم به ریکویست دست پیدا کنیم 
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

class VendorUpdateView(LoginRequiredMixin,UpdateView):
    model=Vendor
    template_name='shop/vendor-change-detail.html'
    form_class=VendorChangeDetailForm
    
    #TODO fix this  for Vendor seekers!!!!
    # def dispatch(self, request, *args, **kwargs) :
    #     if int(kwargs.get('pk')) != self.request.user.pk:
    #         return self.handle_no_permission()
    #     if not (request.user.is_manager or request.user.is_owner):
    #         return HttpResponseForbidden("You are not allowed to access this page.")
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) :
        return reverse_lazy('vendors:my-vendor' , kwargs={'pk':self.object.pk})
    

