from django import forms
from .models import Product, ProductImage,Comment
from vendors.models import Vendor


class AddProductModelForm(forms.ModelForm):
    """
    فرم ایجاد محصول جدید
    """
    input_image = forms.ImageField(label='Image')
    vendors = forms.ModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        required=True,
        label="Vendors"
    )

    class Meta:
        model = Product
        exclude=['average_rating','vendor']

    def __init__(self, *args, **kwargs):
        """
        اینجا هم برای اضافه کردن محصول به فروشگاه های
        مربوط به کارنت یوزر ایجاد شده است
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and (self.request.user.user_type == 'owner' or self.request.user.user_type == 'manager'):

            self.fields['vendors'].queryset = Vendor.objects.filter(user=self.request.user.id)

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            ProductImage.objects.create(
                product=product, image=self.cleaned_data['input_image'])
        return product
    
class CommentModelForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['title','description']