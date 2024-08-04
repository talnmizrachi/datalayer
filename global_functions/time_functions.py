from datetime import datetime, timedelta


def last_thursday(date_str):
    # Convert string to datetime object
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    
    # Calculate the day difference from Thursday (3 in weekday, where Monday is 0)
    weekday = date.weekday()
    if weekday >= 3:
        return date - timedelta(days=(weekday - 3))
    else:
        return date - timedelta(days=(weekday + 4))