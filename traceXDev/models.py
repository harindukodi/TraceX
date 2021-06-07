from django.db import models

# Create your models here.
class test_table_new(models.Model):
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=50)

    class Meta:
        db_table = "test_table_new"