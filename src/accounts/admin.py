from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserImage
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'phone_number', 'is_active',
                    'is_staff', 'is_superuser', 'user_type')
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number',
         'password', 'age', 'city', 'user_type')}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number',  'password1', 'password2', "age",
         "city",)}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                                    'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )
    search_fields = ('email', 'full_name',)
    ordering = ('email', 'phone_number',)
    filter_horizontal = ('groups', 'user_permissions',)

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser
    #     if is_superuser:
    #         form.base_fields['is_superuser'].disabled = True
    #     return form


admin.site.register(User, CustomUserAdmin)

@admin.register(UserImage)
class UserImageModelAdmin(admin.ModelAdmin):
    list_display=['title','image','created_at','user']