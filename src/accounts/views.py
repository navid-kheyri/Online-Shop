from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
import random
from kavenegar import *
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
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard:owner-dashboard')
    template_name = 'accounts/change-password.html'


############## for OTP Verification ####################


class OtpRegisterView(View):
    def generate_otp(self):
        return str(random.randint(1000, 9999))

    def send_otp(self, phone_number, otp):
        try:
            api = KavenegarAPI(
                '36636E4153466D5A4E4273615A344C6C6A76506C35306B775933424F4F745353466278634566344D41524D3D')
            params = {
                'receptor': phone_number,
                'template': 'verify-otp',
                'token': otp,
                'type': 'sms',
            }
            response = api.verify_lookup(params)
            print(response)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/otp-register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        print('*****************************')
        if form.is_valid():
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            age = form.cleaned_data.get("age")
            city = form.cleaned_data.get("city")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            otp = self.generate_otp()
            print(otp)
            print('===========================')

            request.session['otp'] = otp
            request.session['email'] = email
            request.session['phone_number'] = phone_number
            request.session['password1'] = password1
            request.session['password2'] = password2
            request.session['age'] = age
            request.session['city'] = city
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            self.send_otp(phone_number, otp)

            if User.objects.filter(email=email) or User.objects.filter(phone_number=phone_number):
                form.add_error(
                    None, 'User with this email or phone number already exists.')
                return render(request, 'accounts/otp-register.html', {'form': form})
            else:
                if password1 != password2:
                    raise ValueError('password is not match')

            return redirect('accounts:verify-otp')
        else:
            return render(request, 'accounts/otp-register.html', {'form': form})
