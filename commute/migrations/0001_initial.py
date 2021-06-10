# Generated by Django 3.1.7 on 2021-06-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='commute_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commute_type', models.CharField(max_length=60)),
                ('commute_name', models.CharField(max_length=100)),
                ('commute_year', models.CharField(max_length=20)),
                ('commute_month', models.CharField(max_length=60)),
                ('commute_day', models.CharField(max_length=20)),
                ('commute_hour', models.CharField(max_length=20)),
                ('commute_minutes', models.CharField(max_length=20)),
                ('commute_ampm', models.CharField(max_length=20)),
                ('commute_alert', models.CharField(max_length=50)),
                ('commute_passenger_count', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'commute_table',
            },
        ),
    ]
