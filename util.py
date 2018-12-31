import datetime


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


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def parse_command(command_list: list, line: str):
    for command in command_list:
        if line.startswith(command):
            args = line.lstrip(command).strip().split()
            return command, args
    return None, None
