from django import forms
from .models import Vendor
from django.contrib.auth import get_user_model

User = get_user_model()


class VendorModelForms(forms.ModelForm):
    class Meta:
        model=Vendor
        exclude=['user','status']

class UserModelForm(forms.ModelForm):
    class Meta:
        model=User
        fields='__all__'