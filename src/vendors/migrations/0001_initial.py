# Generated by Django 4.2 on 2024-08-10 13:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.MaxLengthValidator(11)])),
                ('email', models.EmailField(max_length=254)),
                ('status', models.BooleanField()),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('user', models.ManyToManyField(related_name='vendors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VendorImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='product/%Y/%m/%d/')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='images', to='vendors.vendor')),
            ],
        ),
    ]
