# Generated by Django 5.0.7 on 2024-08-14 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0027_alter_user_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=None, null=True),
        ),
    ]
