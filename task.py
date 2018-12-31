import datetime
from priority_calculator import PriorityCalculator


class Task:
    def __init__(
            self,
            description: str,
            inserted_time: datetime.datetime,
            *,
            due: datetime.datetime=None,
            priority: int=6,
            time_needed: int=15,
            position: str='any',
            time_slot: str='any',
            cancellable: bool=False,
    ):
        self.description = description
        self.inserted_time = inserted_time
        self.due = due or inserted_time + datetime.timedelta(days=7)
        self.priority = priority
        self.time_needed = time_needed
        self.position = position
        self.time_slot = time_slot
        self.cancellable = cancellable

        self.postponed = datetime.timedelta(0)
        self.priority_calculator = PriorityCalculator()

    def postpone(self, delta: datetime.timedelta):
        self.postponed = delta

    def get_priority(self,
                     time: datetime.datetime,
                     position,
                     time_slot,
                     ):
        return self.priority_calculator.calc_priority(self, time, position)

    def to_db_obj(self):
        return {'description': self.description,
                'position': self.position,
                'time_slot': self.time_slot,
                'priority': self.priority,
                'time_needed': self.time_needed,
                'cancellable': self.cancellable,
                'due': self.due,
                'inserted_time': self.inserted_time,
                }


def parse_task(**kwargs):
    return Task(
        description=kwargs['description'],
        inserted_time=kwargs['inserted_time'],
        due=kwargs['due'],
        priority=kwargs['priority'],
        time_needed=kwargs['time_needed'],
        position=kwargs['position'],
        time_slot=kwargs['time_slot'],
        cancellable=kwargs['cancellable'],
    )