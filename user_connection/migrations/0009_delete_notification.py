# Generated by Django 5.0.8 on 2024-08-30 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_connection', '0008_remove_notification_is_read'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
