# Generated by Django 5.0.8 on 2024-08-20 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User_Auth', '0028_alter_user_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Request Pending'), ('Accepted', 'Request Accepted'), ('Rejected', 'Request Rejected'), ('Blocked', 'Blocked')], default='Pending', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receiver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_connections', to='User_Auth.user')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_connections', to='User_Auth.user')),
            ],
        ),
    ]
