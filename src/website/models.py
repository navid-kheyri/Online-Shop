from django.db import models
from django_jalali.db import models as jmodels

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='category/%Y/%m/%d/',blank=True, null=True,default='default.jpg')
    parent=models.ForeignKey('self',null=True, blank=True, on_delete=models.DO_NOTHING, related_name='sub_categories')

class Product(models.Model):
    name= models.CharField(max_length=100)
    quantity_in_stock=models.IntegerField()
    description = models.TextField()
    price=models.DecimalField(decimal_places=2)
    discount=models.DecimalField(decimal_places=0)
    created_at=jmodels.jDateTimeField(auto_now_add=True)
    updated_at=jmodels.jDateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    vendor=models.ForeignKey('Vendor',on_delete=models.CASCADE,related_name='products')
    
    