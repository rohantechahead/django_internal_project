# Generated by Django 5.0.7 on 2024-08-21 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0030_merge_20240822_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]
