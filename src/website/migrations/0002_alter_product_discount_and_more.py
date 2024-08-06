# Generated by Django 4.2 on 2024-08-06 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity_in_stock',
            field=models.PositiveIntegerField(),
        ),
    ]
