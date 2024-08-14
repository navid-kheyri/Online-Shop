from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from accounts.managers import CustomUserManager

# Create your models here.

phone_number_regex = RegexValidator(r'^(09\d{9})$')
# phone_regex=RegexValidator(r'^\d{11}$')


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
    )
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_number_regex])
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPES, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age', 'city', 'phone_number']

    def is_customer(self):
        return self.user_type == 'customer'

    def is_owner(self):
        return self.user_type == 'owner'

    def is_manager(self):
        return self.user_type == 'manager'

    def is_operator(self):
        return self.user_type == 'operator'

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d/')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="images")

    def __str__(self):
        return self.title
