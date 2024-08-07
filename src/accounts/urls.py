from django.urls import path
from .views import CustomLoginView,my_logout,CustomRegisterView

app_name='accounts'

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',my_logout,name='logout'),
    path('register/',CustomRegisterView.as_view(),name='register')
]