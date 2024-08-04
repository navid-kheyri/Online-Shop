from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='category/%Y/%m/%d/',blank=True, null=True,default='default.jpg')
    parent=models.ForeignKey('self',null=True, blank=True, on_delete=models.DO_NOTHING, related_name='sub_category')
