import datetime


def get_current_season_start_year():
    today = datetime.date.today()
    if today.year < 6:
        return today.year - 1
    return today.year
