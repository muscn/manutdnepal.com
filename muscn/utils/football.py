import datetime


def get_current_season_start_year():
    today = datetime.date.today()
    if today.month < 6:
        return today.year - 1
    return today.year

def get_current_season_start():
    return datetime.date(year=get_current_season_start_year(), month=6, day=30)
