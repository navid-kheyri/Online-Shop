from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import CreateView
from .models import Vendor
from .forms import VendorModelForms

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
        response = super().form_valid(form)
        self.object.user.set([self.request.user])
        form.save()
        return response