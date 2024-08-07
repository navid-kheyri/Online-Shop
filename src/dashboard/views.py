from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth import get_user_model

User = get_user_model()



# Create your views here.

class CustomerDetailView (DetailView):
    model=User
    template_name='dashboard/dashboard.html'

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        user_id=self.object
        user=User.objects.get(id=user_id)
        context['user']=user
        return context
