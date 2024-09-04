from typing import Any
from django import forms
from .models import Vendor, VendorImage, VendorRating
from accounts.models import UserImage
from website.models import Product
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from orders.models import OrderItem


User = get_user_model()


class VendorModelForms(forms.ModelForm):
    input_image = forms.ImageField(label='Image')

    class Meta:
        model = Vendor
        exclude = ['user', 'status']

    def save(self, commit=True):
        vendor = super().save(commit=False)
        if commit:
            vendor.save()
            VendorImage.objects.create(
                vendor=vendor, image=self.cleaned_data['input_image'])
        return vendor


class UserModelForm(forms.ModelForm):
    """
    اینجا نمیدونم چرا فیلد پسورد داخل فیلد، عدد نشون میداد که مجبور شدم بصوزت دستی ایجاد و اورراید کنم؟؟؟؟
    فیلد وندور فروشگاهای کارنت یوزر رو میده
    """
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")
    input_image = forms.ImageField(label='Image')

    vendors = forms.ModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        required=True,
        label="Vendors"
    )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'confirm_password',
                  'first_name', 'last_name', 'age', 'city', 'user_type', 'input_image', 'vendors']

    def __init__(self, *args, **kwargs):
        """
        init در اینجا چویس های ما را که 5 تا بود
        بر اساس یوزر تایپی که مشخص کردیم فیلتر میکنه
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and (self.request.user.user_type == 'owner' or self.request.user.user_type == 'manager'):
            self.fields['user_type'].choices = [
                ('manager', 'Manager'),
                ('operator', 'Operator')
            ]
            self.fields['vendors'].queryset = Vendor.objects.filter(
                user=self.request.user.id)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
            self.save_m2m()
            UserImage.objects.create(
                user=user, image=self.cleaned_data['input_image'])
            user.vendors.set(self.cleaned_data['vendors'])

        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class ProductDetailModelForm(forms.ModelForm):
    input_image = forms.ImageField(label='Image',required=False)

    class Meta:
        model = Product
        exclude = ['vendor']
        # fields=['name']

    def __init__(self, *args, **kwargs):
        """
        دسترسی رول های زیر را برای تغیر فیلد های داده شده میبندیم
        self.fields یک دیکشنری از فیلد های فرم است
        """
        self.request = kwargs.pop('request', None)
        super(ProductDetailModelForm, self).__init__(*args, **kwargs)
        if self.request and (self.request.user.user_type == 'operator' or self.request.user.user_type == 'customer'):
            for field in self.fields.values():
                field.disabled = True
        else:
            self.fields['rating_count'].disabled = True
            self.fields['sum_rating'].disabled = True
            self.fields['average_rating'].disabled = True


class VendorChangeDetailForm(forms.ModelForm):
    input_image = forms.ImageField(label='image', required=False)

    class Meta:
        model = Vendor
        exclude = ['created_at', 'user']
        readonly_fields=['rating_count']

    def __init__ (self ,*args, **kwargs):
        self.request = kwargs.pop('request' , None)
        super(VendorChangeDetailForm , self).__init__(*args, **kwargs)
        self.fields['rating_count'].disabled=True
        self.fields['sum_rating'].disabled=True
        self.fields['average_rating'].disabled=True


class VendorRatingForm(forms.ModelForm):
    class Meta:
        model = VendorRating
        fields = ['rating']

class OrderItemModelForm(forms.ModelForm):
    class Meta:
        model=OrderItem
        fields='__all__'