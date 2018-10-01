import datetime
import re

import os

db_url = os.environ.get('MONGO_URL')
slack_token = os.environ.get('SLACK_BOT_TOKEN')


def weekday_str_to_int(weekday: str):
    if weekday == "Monday":
        return 0
    elif weekday == "Tuesday":
        return 1
    elif weekday == "Wednesday":
        return 2
    elif weekday == "Thursday":
        return 3
    elif weekday == "Friday":
        return 4
    elif weekday == "Saturday":
        return 5
    elif weekday == "Sunday":
        return 6
    else:
        raise ValueError("weekday string is expected, but get {}.".format(weekday))


def daterange(d1, d2):
    return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days))
