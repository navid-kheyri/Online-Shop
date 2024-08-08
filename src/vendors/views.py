from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import CreateView
from .models import Vendor
from .forms import VendorModelForms,UserModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class CreateVendor (View):
    def get(self,request):
        pass
        # return render(request,'dashboard/owner-dashboard.html')
        # return render(request,'test.html')
    
class VendorCreateView(CreateView):
    model=Vendor
    template_name='test.html'
    form_class=VendorModelForms
    success_url=reverse_lazy("website:index")

    def form_valid(self,form):
        """
        در اینجا هدف این است که یوزری که لاگین کرده به عنوان مدیر 
        بصورت پیش فرض ثبت شود  پس کد به این صورت نوشته میشود
        """
        response = super().form_valid(form)
        self.object.user.set([self.request.user])
        form.save()
        return response

class EmplpyeeCreateView(CreateView):
    """
    این کلاس برای ایجاد منیجر و اوپراتور توسط مدیر نوشته شده است.
    """
    model=User
    template_name='test.html'
    form_class=UserModelForm
    success_url=reverse_lazy("website:index")

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
        response = super().form_valid(form)
        self.object.is_staff=True
        form.save()
        return response