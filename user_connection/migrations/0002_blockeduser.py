# Generated by Django 5.0.7 on 2024-08-21 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0031_alter_user_phone_no'),
        ('user_connection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blocked_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_to', to='User_Auth.user')),
                ('blocker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_from', to='User_Auth.user')),
            ],
            options={
                'unique_together': {('blocker_id', 'blocked_id')},
            },
        ),
    ]