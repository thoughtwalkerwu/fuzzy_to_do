import datetime
import copy

from util import daterange
from task import Task


class TaskTemplate:
    def __init__(self, model_task):
        self.model_task = model_task

    def generate(self, date: datetime.time):
        task = copy.deepcopy(self.model_task)
        task.due = date
        return task


class FrequentTaskGenBase:
    def __init__(self, **kwargs):
        self.task_base = TaskTemplate(Task(**kwargs['task']))
        self.last_done = kwargs['last_done']

    def generate_task(self, date):
        raise NotImplementedError

    def to_db_obj_base(self):
        return {
            'task': (self.task_base.generate(self.last_done)).to_db_obj(),
            'last_done': self.last_done,
        }


class WeeklyTaskGen(FrequentTaskGenBase):

    # def __init__(self,
    #              task,
    #              frequency: int=1,
    #              weekday: set=(0, 1, 2, 3, 4, 5, 6),
    #              last_done: datetime.date=datetime.date(2018, 1, 1)
    #              ):
    #     super.__init__(task, last_done)
    #     self.frequency = frequency
    #     self.weekday = weekday
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frequency = kwargs['frequency']
        self.weekday = kwargs['weekday']

    def generate_task(self, date: datetime.datetime):
        weekday_delta = date.weekday() - self.weekday
        if weekday_delta < 0:
            weekday_delta = weekday_delta + 7

        return self.task_base.generate(date + datetime.timedelta(weekday_delta + 7 * (self.frequency - 1)))

    def to_db_obj(self):
        db_obj = self.to_db_obj_base()
        db_obj['frequency'] = self.frequency
        db_obj['weekday'] = self.weekday
        db_obj['task_type'] = "Weekly"
        return db_obj


class UnscheduledTaskGen(FrequentTaskGenBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frequency = kwargs['frequency']

    def generate_task(self, date):
        return self.task_base.generate(date + datetime.timedelta(self.frequency))

    def to_db_obj(self):
        db_obj = self.to_db_obj_base()
        db_obj['frequency'] = self.frequency
        db_obj['task_type'] = "Unscheduled"
        return db_obj

