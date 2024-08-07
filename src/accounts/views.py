from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('registerr:test')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(CustomLoginView, self).form_valid(form)