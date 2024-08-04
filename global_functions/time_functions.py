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