from django.contrib import admin
from .models import (Category,Product,ProductImage,Rating,Comment)
# Register your models here.

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display=['name','image','parent']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    exclude=['description']
    ordering=['created_at','discount','vendor']


@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display=['title','image','created_at','product']

@admin.register(Rating)
class RatingModelAdmin(admin.ModelAdmin):
    list_display=['rating','product','user']
    ordering=['rating']