from django import forms
from customers.models import Address


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
