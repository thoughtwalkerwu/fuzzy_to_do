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

        self.postponed = False

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

        if self.due > self.due:
            delta = date - self.due
            priority += delta.days

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