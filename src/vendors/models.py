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


class VendorImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product/%Y/%m/%d/')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.DO_NOTHING, related_name="images")

    def __str__(self):
        return self.title
