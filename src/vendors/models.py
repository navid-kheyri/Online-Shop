from django.db import models
from django.core.validators import (MaxLengthValidator, MinLengthValidator)
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
    user = models.ManyToManyField(
        User, related_name='vendors')
    address = models.TextField()

    def __str__(self):
        return self.name
    
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
