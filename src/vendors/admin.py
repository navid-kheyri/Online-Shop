from django.contrib import admin
from .models import Vendor, VendorImage
# Register your models here.


class VendorImageInline(admin.StackedInline):
    model = VendorImage
    extra = 1

@admin.register(Vendor)
class VendorModelAdmin(admin.ModelAdmin):
    inlines = [VendorImageInline]
    list_display = ['name', 'phone', 'email',
                    'status', 'created_at', 'address']
    ordering = ['status']


@admin.register(VendorImage)
class VendorImageModelAdmin(admin.ModelAdmin):
    list_display=['title','image','created_at','vendor']
