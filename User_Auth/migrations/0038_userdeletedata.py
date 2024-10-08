# Generated by Django 5.0.8 on 2024-09-05 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0037_user_is_block_alter_user_dob_alter_user_phone_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDeleteData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deleted_data', to='User_Auth.user')),
            ],
        ),
    ]
