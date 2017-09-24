import datetime

import pytz
from django.conf import settings


def season(day=None):
    day = day or datetime.date.today()
    if day.month < 7:
        return day.year - 1
    return day.year


def get_current_season_start():
    return datetime.date(year=season(), month=6, day=30)


def get_current_season_start_time():
    tz = pytz.timezone(settings.TIME_ZONE)
    return datetime.datetime.combine(get_current_season_start(), datetime.time(0, 0)).replace(tzinfo=tz).astimezone(tz)
