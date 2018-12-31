import datetime
import pymongo
from task import parse_task, Task
from task_generator_dom import TaskReaderDOM, TaskWriterDOM


class TaskManager:

    def __init__(self,
                 db_url: str,
                 position='any'
                 ):
        self.position = position
        self.time_slot = "any"
        self.tasks = []
        self.task_reader = TaskReaderDOM(db_url)
        self.task_writer = TaskWriterDOM(db_url)
        self.update_task_list()

    def task_exist(self, description: str):
        return filter(lambda x: x.description == description, self.tasks) is not None

    def get_task(self, description: str):
        task = [x for x in self.tasks if x.description == description][0]
        if task is not None:
            return task
        else:
            raise ValueError("Task {} is not found.".format(description))

    def get_task_by_index(self, index: int):
        try:
            return self.tasks[index]
        except:
            raise ValueError("Invalid task index. Input between 0 and {}".format(len(self.tasks) - 1))

    def done_task(self, task, time: datetime.datetime):
        self.task_writer.done_task(task, time)
        self.task_writer.fill_unadded_tasks(time)

    def done_task_by_name(self, description: str, time: datetime.datetime):
        task = self.get_task(description)
        self.done_task(task, time)

    def done_task_by_index(self, index: int, time: datetime.datetime):
        self.done_task(self.get_task_by_index(index), time)

    def update_task_list(self, keep_postpone=True):
        new_tasks = []
        tasks = self.task_reader.find_all()
        for task_json in tasks:
            task = parse_task(**task_json)
            if keep_postpone:
                task.postponed = (t_task.postponed for t_task in self.tasks if task.description == t_task.description)
            new_tasks.append(task)
        self.tasks = new_tasks
        self.update_priority()

    def update_priority(self):
        for task in self.tasks:
            print(self.position)
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

    def add_task(self, task:Task):
        self.task_writer.insert_task(task)

    def insert_generator(self, generator_json: str):
        self.task_writer.insert_generator(generator_json)
        self.task_writer.fill_unadded_tasks(datetime.datetime.now())


if __name__ == "__main__":
    client = pymongo.MongoClient('192.168.100.108', 27017)
    db = client['test_db']
    _task_collection = db.task_list
    _done_collection = db.done_list

    finder = TaskManager(_task_collection)

    print(finder.next(datetime.datetime.now()))
