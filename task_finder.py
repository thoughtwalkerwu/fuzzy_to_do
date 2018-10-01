import datetime
import pymongo
from task import parse_task, Task


class TaskFinder:

    def __init__(self,
                 task_collection: pymongo.collection.Collection,
                 ):
        self.task_collection = task_collection
        self.position = "any"
        self.time_slot = "any"
        self.tasks = []
        self.update_task_list()

    def update_task_list(self):
        self.tasks = []
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
            self.tasks.append(parse_task(**task_json))
        print(self.tasks)

    def change_position(self, new_position: str):
        self.position = new_position

    def change_time_slot(self, new_time_slot: str):
        self.time_slot = new_time_slot

    def next(self, now: datetime.datetime):
        highest_task = None
        highest_priority = 0

        for task in self.tasks:
            priority = task.get_priority(now, self.position, self.time_slot)

            if priority > highest_priority and not task.postponed:
                highest_priority = priority
                highest_task = task

        # debug
        print(highest_priority)

        return highest_task

    def postpone(self, task: Task):
        task.postponed = True


if __name__ == "__main__":
    client = pymongo.MongoClient('192.168.100.108', 27017)
    db = client['test_db']
    _task_collection = db.task_list
    _done_collection = db.done_list

    finder = TaskFinder(_task_collection)

    print(finder.next(datetime.datetime.now()))
