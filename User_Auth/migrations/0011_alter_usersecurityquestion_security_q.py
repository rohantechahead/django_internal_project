# Generated by Django 5.0.7 on 2024-08-13 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0010_alter_user_first_name_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersecurityquestion',
            name='security_q',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
