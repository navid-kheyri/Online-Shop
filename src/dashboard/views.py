from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()



# Create your views here.

class CustomerDetailView (DetailView):
    model=User
    template_name='dashboard/dashboard.html'
    success_url= success_url=reverse_lazy('dashboard:index')

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        user_id=self.object
        user=User.objects.get(pk=user_id.id)    
        context['user']=user
        return context
