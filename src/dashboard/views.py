from django.shortcuts import redirect, render
from .forms import AddressModelForm
from django.views.generic import DetailView,CreateView,ListView,UpdateView
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth import get_user_model
from vendors.models import Vendor
from customers.models import Address

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
