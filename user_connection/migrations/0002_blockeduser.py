<<<<<<< HEAD
# Generated by Django 5.0.8 on 2024-08-21 07:17
=======
# Generated by Django 5.0.7 on 2024-08-21 20:31
>>>>>>> main

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ('User_Auth', '0032_merge_20240821_1214'),
=======
        ('User_Auth', '0031_alter_user_phone_no'),
>>>>>>> main
        ('user_connection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
<<<<<<< HEAD
                ('blocked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked', to='User_Auth.user')),
                ('blocker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocker', to='User_Auth.user')),
            ],
            options={
                'unique_together': {('blocker', 'blocked')},
=======
                ('blocked_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_to', to='User_Auth.user')),
                ('blocker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_from', to='User_Auth.user')),
            ],
            options={
                'unique_together': {('blocker_id', 'blocked_id')},
>>>>>>> main
            },
        ),
    ]
