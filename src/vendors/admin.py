from django.contrib import admin
from .models import Vendor, VendorImage
# Register your models here.


@admin.register(Vendor)
class VendorModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email',
                    'status', 'created_at', 'address']
    ordering = ['status']


@admin.register(VendorImage)
class VendorImageModelAdmin(admin.ModelAdmin):
    exclude = ['description']
