from django.db import models


# Create your models here.
class user_info_table(models.Model):
    user_email = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_access_level = models.CharField(max_length=100)

    class Meta:
        db_table = "user_info_table"
