from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import *
User = get_user_model()

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


class CustomRegisterView(View):
    template_name='accounts/login.html'
    
    def get(self,request):
        return render (request , self.template_name)
    
    def post(self,request):
        email = request.POST.get("register-email")
        phone_number = request.POST.get("register-phone-number")
        password = request.POST.get("register-password")
        password_confirmation = request.POST.get("register-password-2")
        age = request.POST.get("register-age")
        city = request.POST.get("register-city")
        first_name = request.POST.get("register-first-name")
        last_name = request.POST.get("register-last-name")

        if User.objects.filter(email=email) or User.objects.filter(phone_number=phone_number):
            message = 'Email or Phone Number already exists!'
        else:
            if password != password_confirmation:
                raise ValueError('password is not match')
            
            user = User.objects.create_user(email=email,phone_number=phone_number,
                                            password=password,
                                            age=age,city=city,first_name=first_name,last_name=last_name)
            
            user.save()
            return redirect('/')
        
        return render (request , self.template_name,context={'message':message})
    



class RegisterOwner(View):
    template_name='accounts/owners-register.html'

    def get(self,request):
        return render (request , self.template_name)

    def post(self,request):
        email = request.POST.get("register-email")
        phone_number = request.POST.get("register-phone-number")
        password = request.POST.get("register-password")
        password_confirmation = request.POST.get("register-password-2")
        age = request.POST.get("register-age")
        city = request.POST.get("register-city")
        first_name = request.POST.get("register-first-name")
        last_name = request.POST.get("register-last-name")

        if User.objects.filter(email=email) or User.objects.filter(phone_number=phone_number):
            message = 'Email or Phone Number already exists!'
        else:
            if password != password_confirmation:
                raise ValueError('password is not match')
            
            user = User.objects.create_user(email=email,phone_number=phone_number,
                                            password=password,
                                            age=age,city=city,first_name=first_name,last_name=last_name)
            
            user.user_type='owner'
            user.is_staff=True
            
            user.save()
            return redirect('')
        
        return render (request , self.template_name,context={'message':message})