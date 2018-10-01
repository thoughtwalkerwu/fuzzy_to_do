import datetime


class Task:
    def __init__(self, **kwargs):

        self.description= kwargs['description']
        self.position = kwargs['position']
        self.time_slot = kwargs['time_slot']
        self.priority = kwargs['priority']
        self.time_needed = kwargs['time_needed']
        self.cancellable = kwargs['cancellable']
        self.due = kwargs['due']

        self.postponed = datetime.timedelta(0)

    def postpone(self, delta: datetime.timedelta):
        self.postponed = delta

    def get_priority(self,
                     date: datetime.datetime,
                     position,
                     time_slot,
                     ):
        priority = self.priority

        if self.position == position:
            priority += 3
        if self.time_slot == time_slot:
            priority += 3

        # Due priority calculation
        theo_delta = self.due - date
        delta_days = max(theo_delta.total_seconds()/(60*60*24) + 5/self.priority, 0.1)

        priority += 10/delta_days

        if self.postponed:
            priority -= 1

        return priority

    def to_db_obj(self):
        return {'description': self.description,
                'position': self.position,
                'time_slot': self.time_slot,
                'priority': self.priority,
                'time_needed': self.time_needed,
                'cancellable': self.cancellable,
                'due': self.due,
                }


def parse_task(**kwargs):
    return Task(**kwargs)