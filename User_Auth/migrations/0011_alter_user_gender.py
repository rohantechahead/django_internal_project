# Generated by Django 5.0.8 on 2024-08-13 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0010_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
