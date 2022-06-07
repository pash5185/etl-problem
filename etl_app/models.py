from django.db import models

# Create your models here.
class SampleData(models.Model):
    product_name = models.CharField(max_length=255)
    quality = models.CharField(max_length=50)
    material_name = models.CharField(max_length=50)
    worth = models.FloatField()
    file_source = models.TextField()