from django.db import models
from django.core.validators import (MinLengthValidator, MaxLengthValidator)
from django.contrib.auth.models import User

# Create your models here.


class Address(models.Model):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10, blank=True,
                               validators=[
                                   MinLengthValidator(10),
                                   MaxLengthValidator(10)
                               ])
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return f"{self.id} {self.state}, {self.city}, {self.street}"
