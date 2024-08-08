from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import View

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
        context['user']=user
        return context

class OwnerDashboardView (View):
    """
    برای نشان دادن داشبورد مدیز
    """
    #TODO complet this
    def get(self,request):
        return render(request,'dashboard/owner-dashboard.html')
        # return render(request,'test.html')