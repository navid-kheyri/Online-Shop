from django.contrib import admin
from .models import (Category,Product,ProductImage,Rating,Comment)
# Register your models here.

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display=['name','image','parent']
