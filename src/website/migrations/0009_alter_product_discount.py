# Generated by Django 4.2 on 2024-08-28 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_product_rating_count_product_sum_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True),
        ),
    ]
