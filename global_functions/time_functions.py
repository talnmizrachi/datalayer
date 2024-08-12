import os
from global_functions.LoggingGenerator import Logger
from datetime import datetime, timedelta
logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def last_thursday_getter(date_str):
    # Convert string to datetime object
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    logger.info(f"date: {date}")
    logger.info(f"date: {type(date)}")
    
    # Calculate the day difference from Thursday (3 in weekday, where Monday is 0)
    weekday = date.weekday()
    if weekday >= 3:
        return date - timedelta(days=(weekday - 3))
    else:
        return date - timedelta(days=(weekday + 4))

    
def utc_to_date(utc_timestamp):
    if isinstance(utc_timestamp, str):
        return utc_timestamp
    if utc_timestamp is not None:
        # Convert from milliseconds to seconds if necessary
        # This checks if the timestamp is far greater than typical Unix epoch time in seconds
        if utc_timestamp > 1e12:
            utc_timestamp /= 1000
        return datetime.utcfromtimestamp(utc_timestamp).date()
    else:
        # Return today's date plus 7 days
        return datetime.utcnow().date() + timedelta(days=7)
