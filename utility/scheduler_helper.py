from datetime import datetime, timedelta
from django.utils.timezone import now


def check_and_send_reminders():
    current_time = now()