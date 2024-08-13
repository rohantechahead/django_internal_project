# Generated by Django 5.0.8 on 2024-08-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='DOB',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_no',
            field=models.IntegerField(default=0),
        ),
    ]
