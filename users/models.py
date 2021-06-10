from django.db import models


# Create your models here.
class user_tracking_table(models.Model):
    user_email = models.CharField(max_length=100)
    commute_type = models.CharField(max_length=100)
    commute_name = models.CharField(max_length=100)
    commute_year = models.CharField(max_length=20)
    commute_month = models.CharField(max_length=60)
    commute_day = models.CharField(max_length=20)
    commute_hour = models.CharField(max_length=20)
    commute_minutes = models.CharField(max_length=20)
    commute_ampm = models.CharField(max_length=20)
    commute_alert = models.CharField(max_length=50)

    class Meta:
        db_table = "user_tracking_table"
