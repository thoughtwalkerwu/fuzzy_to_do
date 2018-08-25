import datetime
import re
import pymongo


class MorningTask:
    TASK_COMMAND = "morning"

    def __init__(self, db_collection: pymongo.collection.Collection, morning: datetime.time):
        self.hour = morning.hour
        self.minute = morning.minute
        self.collection = db_collection

    def add_task(self, description: str, frequency: str="everyday", cancellable: bool=True, priority: int=5):
        post = {
            "description": description,
            "time_slot": "morning",
            "frequency": frequency,
            "cancellable": cancellable,
            "priority": priority
        }
        self.collection.insert_one(post)

    def add_once_task(self, description: str, cancellable: bool=True, priority: int=5):
        self.add_task(description, frequency="once", cancellable=cancellable, priority=priority)

    def handle_request(self, command, condition):
        response = ""
        if command == self.TASK_COMMAND:
            response += "朝のタスク一覧\n"
            for task in self.collection.find({"time_slot": condition['time_slot'], "position": condition['position']}):
                response += task["description"] + "\n"
        elif command.startswith(self.TASK_COMMAND):

            task_name = re.sub(self.TASK_COMMAND + " ", "", command)
            self.add_task(task_name)
            print(task_name)
            response += task_name + "is added"
        return response

    def is_morning(self, now: datetime.time):
        print(now.minute == self.minute)
        print(now.second == 0)
        if self.hour == now.hour and self.minute == now.minute and now.second == 0:
            print("morning now")
            return True


class DailyTask:
    TASK_COMMAND = "daily"

    def __init__(self, db_collection: pymongo.collection.Collection):
        self.collection = db_collection

    def add_task(self,
                 description: str,
                 position: str="home",
                 time_slot: str='any',
                 priority: int=5,
                 time_needed: int=10,
                 frequency: int=1,
                 weekday: set=(0, 1, 2, 3, 4, 5, 6),
                 cancellable: bool=False,
                 before: int=None,
                 after: int=None,
                 due: datetime.date=None,
                 schedule: str=None,
                 grouping: str=None,
                 cost: int=0
                 ):
        post = {
            "description": description,
            "time_slot": time_slot,
            "schedule": schedule,
            "time_needed": time_needed,
            "frequency": frequency,
            "weekday": weekday,
            "before": before,
            "after": after,
            "due": due,
            "cancellable": cancellable,
            "position": position,
            "grouping": grouping,
            "priority": priority,
            "cost": cost,
            'closed': False
        }
        self.collection.insert_one(post)

    def handle_request(self, command, task_condition):
        if task_condition is None:
            condition = {'time_slot': "any", 'position': "any"}
        else:
            condition = task_condition

        response = ""
        if command == self.TASK_COMMAND:
            response += "今日のタスク一覧\n"
            for task in self.collection.find({"time_slot": condition['time_slot'], "position": condition['position']}):
                response += task["description"] + "\n"
        elif command.startswith(self.TASK_COMMAND):

            task_name = re.sub(self.TASK_COMMAND + " ", "", command)
            self.add_task(task_name)
            print(task_name)
            response += task_name + "is added"
        return response


class TaskBase:
    TASK_COMMAND = "task"

    def __init__(self, db_collection: pymongo.collection.Collection):
        self.collection = db_collection

    def add_task(self,
                 description: str,
                 position: str="home",
                 time_slot: str='any',
                 priority: int=5,
                 time_needed: int=10,
                 frequency: int=1,
                 weekday: set=(0, 1, 2, 3, 4, 5, 6),
                 cancellable: bool=False,
                 before: datetime.time=None,
                 after: datetime.time=None,
                 due: datetime.date=None,
                 schedule: str=None,
                 grouping: str=None,
                 ):
        post = {
            "description": description,
            "time_slot": time_slot,
            "schedule": schedule,
            "time_needed": time_needed,
            "frequency": frequency,
            "weekday": weekday,
            "before": before,
            "after": after,
            "due": due,
            "cancellable": cancellable,
            "position": position,
            "grouping": grouping,
            "priority": priority,
            'closed': False
        }
        self.collection.insert_one(post)