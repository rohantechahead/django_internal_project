# Generated by Django 5.0.8 on 2024-08-24 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_connection', '0005_blockeduser_is_block'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blockeduser',
            name='is_block',
        ),
    ]