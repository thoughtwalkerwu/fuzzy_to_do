import datetime
import re

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
        raise ValueError("weekday string is expected, but get {}.".format(weekday)

# def get_schedule_priority_func(schedule: str):
#     frequent_match = re.match("^every (?P<days>\d+)days$", schedule):
#     if frequent_match:
#         frequency = int(frequent_match.group('days'))
#         def priority_func(last_done: datetime.datetime, now:datetime.datetime):
#             return max((now - last_done).days - frequency, 0)
#         return priority_func
#
#     if re.match("^every (?P<days>\d+)days$", schedule):
#
#         elif sch_body.endswith("day"):
#             if now.weekday():
#     elif sch_type == "at":
#
#     elif sch_type == "due":
#
#
#     else:
#         return 0