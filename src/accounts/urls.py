from django.urls import path
from .views import CustomLoginView,my_logout

app_name='accounts'

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',my_logout,name='logout'),
]