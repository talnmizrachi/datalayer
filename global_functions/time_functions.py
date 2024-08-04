from datetime import datetime, timedelta


def last_thursday_getter(date):
    # Calculate the day difference from Thursday (3 in weekday, where Monday is 0)
    weekday = date.weekday()
    if weekday >= 3:
        return date - timedelta(days=(weekday - 3))
    else:
        return date - timedelta(days=(weekday + 4))
    