from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import CustomUser, UserImage
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["email", "phone_number"]


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    input_image = forms.ImageField(label='Image')

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number',
                  'first_name', 'last_name', 'age', 'city', 'user_type', 'input_image']

    def __init__(self, *args, **kwargs):
        """
        دسترسی رول های زیر را برای تغیر فیلد های داده شده میبندیم
        """
        self.request = kwargs.pop('request', None)
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        if self.request and (self.request.user.user_type == 'owner' or self.request.user.user_type == 'operator' or self.request.user.user_type == 'manager' or self.request.user.user_type == 'customer'):
            self.fields['user_type'].disabled = True
            self.fields['email'].disabled = True
            self.fields['phone_number'].disabled = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserImage.objects.create(
                user=user, image=self.cleaned_data['input_image'])
        return user
