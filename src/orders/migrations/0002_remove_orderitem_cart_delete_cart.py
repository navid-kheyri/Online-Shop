# Generated by Django 4.2 on 2024-08-19 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='cart',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
