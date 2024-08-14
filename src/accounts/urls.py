from django.urls import path
from .views import (CustomLoginView,my_logout,CustomRegisterView,RegisterOwner,EmployeeUpdateView,ChangePasswordView,
                    OtpRegisterView,VerifyOtpView
                    )

app_name='accounts'

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',my_logout,name='logout'),
    path('register/',CustomRegisterView.as_view(),name='register'),
    path('register_owner/',RegisterOwner.as_view(),name='register-owner'),
    path('edit_employee/<pk>/',EmployeeUpdateView.as_view(),name='edit-employee'),
    path('change_password/',ChangePasswordView.as_view(),name='change-password'),
    path('otp_register/',OtpRegisterView.as_view(),name='otp-register'),
    path('verify_otp/',VerifyOtpView.as_view(),name='verify-otp')

]