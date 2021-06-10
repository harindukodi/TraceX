from django.db import models


# Create your models here.
class commute_table(models.Model):
    commute_type = models.CharField(max_length=60)
    commute_name = models.CharField(max_length=100)
    commute_date = models.CharField(max_length=60)
    commute_time = models.CharField(max_length=100)
    commute_alert = models.CharField(max_length=50)
    commute_passenger_count = models.CharField(max_length=30)

    class Meta:
        db_table = "commute_table"
