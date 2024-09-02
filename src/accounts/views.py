from django.http import HttpRequest, HttpResponseForbidden
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.utils.decorators import method_decorator
from .decorators import roles_required
import random
from kavenegar import *
from django.contrib.auth.mixins import LoginRequiredMixin
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
                # raise ValueError('password is not match')
                message='password is not match'
                return render(request, self.template_name,context={'messeage':message})

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


class EmployeeUpdateView(LoginRequiredMixin,UpdateView):
    """
    برای آپدیت کردن اطلاعات کارمندان
    """
    def dispatch(self, request, *args, **kwargs) :
        if int(kwargs.get('pk')) != self.request.user.pk:
            return self.handle_no_permission()
        if not (request.user.is_owner or request.user.is_operator or request.user.is_manager):
            return HttpResponseForbidden("You are not allowed to access this page.")
        return super().dispatch(request, *args, **kwargs)

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

@method_decorator( roles_required('manager','operator','owner') , name='dispatch')
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard:owner-dashboard')
    template_name = 'accounts/change-password.html'


############## for OTP Verification ####################


def generate_otp():
    return str(random.randint(1000, 9999))


def send_otp(phone_number, otp):
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


class OtpRegisterView(View):
    """
    برای رجیستر کاربر معمولی با OTP
    """

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
            otp = generate_otp()
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
            send_otp(phone_number, otp)

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


class VerifyOtpView(View):
    """
    برای تایید کد تایید با OTP
    """

    def get(self, request):
        form = OTPForm()
        return render(request, 'accounts/verify-otp.html', {'form': form})

    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            stored_otp = request.session.get('otp')
            if entered_otp == stored_otp:
                phone_number = request.session.get('phone_number')
                email = request.session.get('email')
                age = request.session.get('age')
                city = request.session.get('city')
                first_name = request.session.get('first_name')
                last_name = request.session.get('last_name')
                password1 = request.session.get('password1')

                user = User.objects.create_user(email=email, phone_number=phone_number, password=password1,
                                                age=age, city=city, first_name=first_name, last_name=last_name)
                user.save()
                # >>>>>age boden pass bekhaim<<<<
                # user, created = User.objects.get_or_create(email=email, phone_number=phone_number,age=age,city=city,first_name=first_name,last_name=last_name)
                # if created:
                #     user.set_unusable_password()
                #     user.save()

                return redirect('/')
            else:
                return render(request, 'accounts/verify-otp.html', {'error': 'کد تایید شما نامعتبر است'})

        else:
            return render(request, 'accounts/verify-otp.html', {'form': form})


class OtpLoginView(View):
    """
    برای ورود با OTP
    """

    def get(self, request):
        form = PhoneNumberForm()
        return render(request, 'accounts/otp-login.html', {'form': form})

    def post(self, request):
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = request.POST.get('phone_number')
            otp = generate_otp()
            print(otp)
            print('++++++++++++++++++++++++++++')
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            send_otp(phone_number, otp)
            return redirect('accounts:verify-login-otp')
        return render(request, 'accounts/otp-login.html', {'form': form})


class VerifyLoginOtpView(View):
    """
    برای تایید کد تایید با OTP 
    """

    def get(self, request):
        form = OTPForm()
        return render(request, 'accounts/verify-login-otp.html', {'form': form})

    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            stored_otp = request.session.get('otp')
            entered_otp = form.cleaned_data.get('otp')
            phone_number = request.session.get('phone_number')
            if entered_otp == stored_otp:
                user, created = User.objects.get_or_create(
                    phone_number=phone_number)
                login(request, user)
                if request.user.user_type == 'customer':
                    return redirect("website:index")
                elif (user.user_type == 'owner' or user.user_type == 'manager' or user.user_type == 'operator'):
                    return redirect("dashboard:owner-dashboard")
            else:
                form.add_error('otp', 'Invalid OTP')

        return render(request, 'accounts/otp-login.html', {'form': form})
