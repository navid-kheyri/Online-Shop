from django.db import models
from django.core.validators import (MaxLengthValidator, MinLengthValidator,MaxValueValidator, MinValueValidator)

from django_jalali.db import models as jmodels
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=11,
                             validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    email = models.EmailField()
    status = models.BooleanField()
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    rating_count = models.IntegerField(default=0)
    sum_rating = models.IntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00,validators=[
                                            MinValueValidator(1.0), 
                                            MaxValueValidator(5.0)
                                        ])
    user = models.ManyToManyField(
        User, related_name='vendors')
    address = models.TextField()

    def __str__(self):
        return self.name
    
    def update_average_rating(self):
        if self.rating_count > 0:
            self.average_rating = round(self.sum_rating / self.rating_count, 1)
    
    def save(self, *args, **kwargs):
        if not self.status:
            self.status = True
        super().save(*args, **kwargs)


class VendorImage(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d/',default='default.jpg')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.image.url
    

class VendorRating(models.Model):
    rating = models.IntegerField(default=1, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vendor_ratings')
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='ratings')
    
    def __str__(self):
        return str(self.rating)
    
    def save(self, *args, **kwargs):
        self.vendor.rating_count += 1  
        self.vendor.sum_rating += self.rating
        self.vendor.update_average_rating()
        self.vendor.save()
        super().save(*args, **kwargs)

    
    

