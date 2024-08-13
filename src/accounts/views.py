from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class CustomLoginView(View):
    """
    لاگین کاستومر و مدیر در اینجا انجام میشود و هر کدام به صفحه خود هدایت میشوند.
    """
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("singin-email")
        password = request.POST.get("singin-password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if request.user.user_type == 'customer':
                return redirect("website:index")
            elif (user.user_type == 'owner' or user.user_type == 'manager' or user.user_type == 'operator'):
                print(user.user_type)
                print('***================================')
                return redirect("dashboard:owner-dashboard")

        return render(request, self.template_name)

# TODO CBV later


@login_required
def my_logout(request):
    logout(request)
    return redirect('/')


class CustomRegisterView(View):

    """
    صفحه مربوط به رجیستر کاستومر
    """
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
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

            user = User.objects.create_user(email=email, phone_number=phone_number,
                                            password=password,
                                            age=age, city=city, first_name=first_name, last_name=last_name)

            user.save()
            return redirect('/')

        return render(request, self.template_name, context={'message': message})


class RegisterOwner(View):
    """
    صفحه مربوط به رجیستر مدیر
    """
    template_name = 'accounts/owners-register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
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

            user = User.objects.create_user(email=email, phone_number=phone_number,
                                            password=password,
                                            age=age, city=city, first_name=first_name, last_name=last_name)

            user.user_type = 'owner'
            user.is_staff = True

            user.save()
            return redirect('dashboard:owner-dashboard')
            # return redirect('vendors:create_vendor')

        return render(request, self.template_name, context={'message': message})


class EmployeeUpdateView(UpdateView):
    """
    برای آپدیت کردن اطلاعات کارمندان
    """
    model = User
    template_name = 'accounts/edit-employee.html'
    success_url = reverse_lazy('dashboard:owner-dashboard')
    form_class = CustomUserChangeForm

    def get_form_kwargs(self):
        """
        در اینجا ما در واقع  ریکوئست را به فرم پاس میدهیم  
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ChangePasswordView(PasswordChangeView):
    form_class=PasswordChangeForm
    success_url = reverse_lazy('dashboard:owner-dashboard')
    template_name='accounts/change-password.html'