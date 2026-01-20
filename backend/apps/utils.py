"""
Utility functions for the hospital management system.
Includes timezone helpers to ensure consistent IST (Asia/Kolkata) usage.
"""
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from datetime import datetime, timedelta
import pytz


def get_ist_now():
    """
    Get current datetime in IST (Asia/Kolkata) timezone.
    
    Returns:
        datetime: Current datetime in IST timezone
    """
    local_tz = pytz.timezone(settings.TIME_ZONE)
    return timezone.now().astimezone(local_tz)


def get_ist_today():
    """
    Get current date in IST (Asia/Kolkata) timezone.
    
    Returns:
        date: Current date in IST timezone
    """
    return get_ist_now().date()


def get_ist_date_range():
    """
    Get datetime range for today in IST timezone.
    Returns start and end of today (midnight to midnight) in IST.
    
    Returns:
        tuple: (start_datetime, end_datetime) for today in IST
    """
    local_tz = pytz.timezone(settings.TIME_ZONE)
    today = get_ist_today()
    
    # Create start of day (00:00:00) in IST
    start_of_day = local_tz.localize(datetime.combine(today, datetime.min.time()))
    
    # Create end of day (23:59:59) in IST
    end_of_day = local_tz.localize(datetime.combine(today, datetime.max.time()))
    
    return start_of_day, end_of_day


def convert_to_ist(dt):
    """
    Convert a datetime to IST (Asia/Kolkata) timezone.
    
    Args:
        dt: datetime object to convert
        
    Returns:
        datetime: Datetime in IST timezone
    """
    local_tz = pytz.timezone(settings.TIME_ZONE)
    if dt.tzinfo is None:
        # If naive datetime, assume it's in UTC and make it aware
        dt = timezone.make_aware(dt, timezone.utc)
    return dt.astimezone(local_tz)
