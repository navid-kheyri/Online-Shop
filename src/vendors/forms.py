from django import forms
from .models import Vendor
from django.contrib.auth import get_user_model


User = get_user_model()


class VendorModelForms(forms.ModelForm):
    class Meta:
        model=Vendor
        exclude=['user','status']

class UserModelForm(forms.ModelForm):
    """
    اینجا نمیدونم چرا فیلد پسورد داخل فیلد، عدد نشون میداد که مجبور شدم بصوزت دستی ایجاد و اورراید کنم؟؟؟؟
    """
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    class Meta:
        model=User
        fields=['email','phone_number','password','confirm_password','first_name','last_name','age','city','user_type']
        
    def __init__(self, *args, **kwargs):
        """
        init در اینجا چویس های ما را که 5 تا بود
        بر اساس یوزر تایپی که مشخص کردیم فیلتر میکنه
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.user_type == 'owner':
            self.fields['user_type'].choices = [
                ('manager', 'Manager'),
                ('operator', 'Operator')
            ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data