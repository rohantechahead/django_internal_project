# Generated by Django 5.0.8 on 2024-08-12 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0007_user_is_login_user_refresh_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='DOB',
            new_name='dob',
        ),
    ]