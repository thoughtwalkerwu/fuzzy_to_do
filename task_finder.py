import datetime
import pymongo
from task import parse_task, Task
from task_generator_dom import done_task
from functools import reduce

class TaskFinder:

    def __init__(self,
                 task_collection: pymongo.collection.Collection,
                 ):
        self.task_collection = task_collection
        self.position = "any"
        self.time_slot = "any"
        self.tasks = []
        self.update_task_list()

    def task_exist(self, description: str):
        return filter(lambda x: x.description == description, self.tasks) is not None

    def get_task(self, description: str):
        return [x for x in self.tasks if x.description == description][0]

    def get_task_by_index(self, index: int):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        else:
            return None

    def done_task_by_name(self, description: str, time: datetime.datetime):
        task = self.get_task(description)
        if task is not None:
            done_task(task, time)
        else:
            raise ValueError("Task {} is not found.".format(description))

    def done_task_by_index(self, index: int, time: datetime.datetime):
        task = self.get_task_by_index(index)
        if task is not None:
            done_task(task, time)
        else:
            raise ValueError("Invalid task index. Input between 0 and {}".format(len(self.tasks) - 1))

    def update_task_list(self, keep_postpone=True):
        new_tasks = []
        tasks = self.task_collection.find(

            # {
            #     '$or': [{'position': self.position, 'position': "any"}]
            #  },
            # {
            #     '$or': [{'time_slot': self.position, 'time_slot': "any"}]
            # }#,
            # # {
            # #     "close": False
            # # }
        )
        for task_json in tasks:
            task = parse_task(**task_json)
            if keep_postpone:
                task.postponed = (t_task.postponed for t_task in self.tasks if task.description == t_task.description)
            new_tasks.append(task)
        self.tasks = new_tasks
        self.update_priority()

    def update_priority(self):
        for task in self.tasks:
            task.priority = task.get_priority(datetime.datetime.now(), self.position, self.time_slot)
        self.tasks.sort(key=lambda x: x.priority, reverse=True)

    def change_position(self, new_position: str):
        self.position = new_position

    def change_time_slot(self, new_time_slot: str):
        self.time_slot = new_time_slot

    def next(self, now: datetime.datetime):
        return self.tasks[0]

    def postpone(self, task: Task):
        task.postponed = True

    def top(self, num: int=10):
        length = min(len(self.tasks), num)
        return self.tasks[0:length]


if __name__ == "__main__":
    client = pymongo.MongoClient('192.168.100.108', 27017)
    db = client['test_db']
    _task_collection = db.task_list
    _done_collection = db.done_list

    finder = TaskFinder(_task_collection)

    print(finder.next(datetime.datetime.now()))
