from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class CustomLoginView(View):
    template_name = 'accounts/login.html'

    def get(self,request):
        return render (request , self.template_name)
    
    def post(self,request):      
        email = request.POST.get("singin-email")
        password = request.POST.get("singin-password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("website:index")

        return render(request, self.template_name)
    
@login_required
def my_logout(request):
    logout(request)
    return redirect ('/')