import datetime
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from django.utils import timezone

from User_Auth.models import User, UserDeleteData
from user_connection.models import UserConnection
from user_notification.models import Notification


def send_birthday_reminders():
    try:
        today = timezone.now().date()
        birthday_users = User.objects.filter(dob=today)
        for user in birthday_users:
            sender_friends_ids = UserConnection.objects.filter(
                sender_id=user.id,
                status='Accepted'
            ).values_list('receiver_id', flat=True)

            receiver_friends_ids = UserConnection.objects.filter(
                receiver_id=user.id,
                status='Accepted'
            ).values_list('sender_id', flat=True)

            friends_ids = set(sender_friends_ids) | set(receiver_friends_ids)
            friends = User.objects.filter(id__in=friends_ids).distinct()
            for friend in friends:
                notification = Notification(
                    sender=user,
                    receiver=friend,
                    message=f"Today is {user.username}'s birthday!",
                    notification_type='Reminder',
                )
                notification.save()

    except Exception as e:
        print(f"An error occurred in send_birthday_reminders: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    trigger_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    scheduler.add_job(
        send_birthday_reminders,
        trigger=DateTrigger(run_date=trigger_time),
        id='birthday_reminder_job',
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
    job = scheduler.get_job('bi'
                            'rthday_reminder_job')
    if job:
        print(f"Job added successfully: {job}")
    else:
        print("Job not added.")


start_scheduler()


def check_deleted_users():
    try:
        current_time = timezone.now()
        expired_users = UserDeleteData.objects.filter(deleted_date__lte=current_time).values_list('user_id', flat=True)

        User.objects.get(id__in=expired_users).delete()

        print("Deleted expired users successfully.")
    except Exception as e:
        print(f"An error occurred in check_deleted_users: {e}")


def check_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        check_deleted_users,
        'interval',
        days=1,
        id='check_deleted_users_job',
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
    job = scheduler.get_job('check_deleted_users_job')
    if job:
        print(f"Job added successfully: {job}")
    else:
        print("Job not added.")


check_scheduler()
