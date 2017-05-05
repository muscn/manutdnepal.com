import datetime

import pytz
from django.conf import settings


def get_current_season_start_year():
    today = datetime.date.today()
    if today.month < 6:
        return today.year - 1
    return today.year


def get_current_season_start():
    return datetime.date(year=get_current_season_start_year(), month=6, day=30)


def get_current_season_start_time():
    tz = pytz.timezone(settings.TIME_ZONE)
    return datetime.datetime.combine(get_current_season_start(), datetime.time(0, 0)).replace(tzinfo=tz).astimezone(tz)
