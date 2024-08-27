# Generated by Django 5.0.8 on 2024-08-26 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0036_remove_user_is_block_alter_user_dob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_block',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]