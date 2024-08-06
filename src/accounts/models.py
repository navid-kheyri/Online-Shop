from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from accounts.managers import CustomUserManager

# Create your models here.

phone_number_regex = RegexValidator(r'^(09\d{9})$')
# phone_regex=RegexValidator(r'^\d{11}$')


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_number_regex])
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age', 'city', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
