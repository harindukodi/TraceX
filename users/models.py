from django.db import models


# Create your models here.
class user_tracking_table(models.Model):
    user_email = models.CharField(max_length=100)
    commute_type = models.CharField(max_length=100)
    commute_name = models.CharField(max_length=100)
    commute_date = models.CharField(max_length=100)
    commute_time = models.CharField(max_length=100)
    commute_alert = models.CharField(max_length=50)

    class Meta:
        db_table = "user_tracking_table"
