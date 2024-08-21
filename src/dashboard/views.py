from django.shortcuts import get_object_or_404, redirect, render
from .forms import AddressModelForm
from django.views.generic import DetailView,CreateView,ListView,UpdateView
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth import get_user_model
from vendors.models import Vendor
from customers.models import Address
from accounts.forms import CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from orders.models import Order,OrderItem
from website.models import Comment
from django.utils.decorators import method_decorator
from accounts.decorators import roles_required

User = get_user_model()



# Create your views here.

class CustomerDetailView (DetailView):
    """
    برای نشان دادن داشبورد کاستومر
    """
    model=User
    template_name='dashboard/dashboard.html'
    success_url= success_url=reverse_lazy('dashboard:index')

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        user_id=self.object
        user=User.objects.get(pk=user_id.id)
        addresses=user.address.all()
        context['address_form']=AddressModelForm()
        context['address']=addresses
        context['user']=user
        return context

    def post(self,request,*args,**kwargs):
        form=AddressModelForm(request.POST)
        if form.is_valid():
            address= form.save(commit=False)
            address.user=self.request.user
            address.save()
            return redirect('dashboard:user',pk=self.get_object().id)
        return self.get(request,*args,**kwargs)
    

# class OwnerDashboardView (View):
#     """
#     برای نشان دادن داشبورد مدیز
#     """
#     #TODO complet this
#     def get(self,request):
#         return render(request,'dashboard/owner-dashboard.html')
#         # return render(request,'test.html')


class MyVendorListView(ListView):
    """
    برای دیدن فروشگاه های خود
    """
    model=Vendor
    template_name='dashboard/owner-dashboard.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        vendor=Vendor.objects.prefetch_related('user').filter(user=user.id)
        context['vendor']=vendor
        return context
    
# class AdressCreateView(CreateView):
#     model=Address
#     template_name=

class CustomerUpdateView(UpdateView):
    model = User
    template_name='dashboard/customer-detail-change.html'
    form_class=CustomUserChangeForm

    def get_success_url(self):
        return reverse_lazy('dashboard:user', kwargs={'pk': self.object.pk})


    # def get_context_data(self, **kwargs) :
    #     context= super().get_context_data(**kwargs)
    #     context['customer_update']=CustomUserChangeForm()

    def get_form_kwargs(self):
        """
        در اینجا ما در واقع  ریکوئست را به فرم پاس میدهیم  
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
class CustomerChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard:user')
    template_name = 'dashboard/customer-change-password.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:user', kwargs={'pk': self.request.user.pk})
    
class CustomerOrdersListView(ListView):
    model=Order
    template_name='dashboard/customer-orders.html'

    def get_queryset(self) :
        user=self.request.user
        user_order=Order.objects.filter(user=user)
        print(user_order)
        return user_order
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['myorder'] = self.get_queryset()
        return context
    

class CustomerOrderItemDetailView(DetailView):
    model=OrderItem
    template_name='dashboard/customer-order-item.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items=OrderItem.objects.filter(order=self.get_object())
        context['order_items'] = order_items
        return context
    

class MyCommentDetailView(DetailView):
    model=Comment
    template_name='dashboard/comments.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return pk

    # chera in ravesh kar nakard????

    # def get_queryset(self) :
    #     user=self.request.user
    #     user_comment=Comment.objects.filter(user=user)
    #     print(user_comment)
    #     return user_comment
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user_comment=Comment.objects.filter(user=self.get_object())
        context['mycomment'] = user_comment
        # context['mycomment'] = self.get_queryset()
        return context