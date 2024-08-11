from django import forms
from .models import Product, ProductImage


class AddProductModelForm(forms.ModelForm):
    """
    فرم ایجاد محصول جدید
    """
    input_image = forms.ImageField(label='Image')

    class Meta:
        model = Product
        exclude=['average_rating']

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            ProductImage.objects.create(
                product=product, image=self.cleaned_data['input_image'])
        return product
