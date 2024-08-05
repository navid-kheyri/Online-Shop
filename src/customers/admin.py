from django.contrib import admin
from .models import Address

# Register your models here.


@admin.register(Address)
class AdressModelAdmin(admin.ModelAdmin):
    list_display = ['state', 'city', 'street', 'zipcode']
