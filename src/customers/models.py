from django.db import models
from django.core.validators import (MinLengthValidator, MaxLengthValidator)

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

    def __str__(self):
        return f"{self.id} {self.state}, {self.city}, {self.street}"
