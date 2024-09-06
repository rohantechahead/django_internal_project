from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Friend_Request', 'Friend Request'), ('Message', 'Message'), ('Reminder', 'Reminder'), ('Tag_Wish', 'Tag Wish')], max_length=20),
        ),
    ]