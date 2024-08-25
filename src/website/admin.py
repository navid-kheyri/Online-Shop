from django.contrib import admin
from .models import (Category, Product, ProductImage, Rating, Comment)
# Register your models here.


class ProductInline(admin.StackedInline):
    model=Product
    extra = 0


class CommenttInline(admin.StackedInline):
    model=Comment
    extra = 0

class RatingInline(admin.StackedInline):
    model=Rating
    extra = 0


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    inlines=[ProductInline]
    list_display = ['name', 'image', 'parent']
    search_fields=['name']


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,CommenttInline,RatingInline]
    list_display = ['name' , 'quantity_in_stock','price','discount','average_rating','category']
    ordering = ['created_at', 'discount']
    search_fields=['name','price','discount','quantity_in_stock']


@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'created_at', 'product']


@admin.register(Rating)
class RatingModelAdmin(admin.ModelAdmin):
    list_display = ['rating', 'product', 'user']
    ordering = ['rating']


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'user', 'created_at','comment_type']
