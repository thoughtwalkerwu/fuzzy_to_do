import datetime
import pymongo


class TaskFinder:

    def __init__(self,
                 task_collection: pymongo.collection.Collection,
                 done_collection: pymongo.collection.Collection
                 ):
        self.task_collection = task_collection
        self.done_collection = done_collection
        self.position = "any"
        self.time_slot = "any"
        self.tasks = self.update_task_list()

    def update_task_list(self):
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
        return tasks

    def change_position(self, new_position: str):
        self.position = new_position

    def change_time_slot(self, new_time_slot: str):
        self.time_slot = new_time_slot

    def next(self, now: datetime.datetime):
        # done list consists of { id, date, type(done/postpawned}

        # total priority = priority
        # for tasks with due, priority += max(0, today - due + 7)
        # for repeating, priority += max(0, today - done date - frequency)
        # priority +3 for same position
        # priority +3 for same time slot
        # priority -= 1 if postponed

        highest_task = None
        highest_priority = 0

        for task in self.tasks:
            priority = task['priority']

            if task['position'] == self.position:
                priority += 3
            if task['time_slot'] == self.time_slot:
                priority += 3

            if task.get('due') is not None and now > task['due']:
                delta = now - task['due']
                priority += delta.days

            if task.get('frequency') is not None:
                last_done = self.done_collection.find_one(
                    {
                        "description": task['description']
                    },
                    sort=[("done_date", -1)]
                )
                if last_done is not None:
                    delta = now - last_done
                    priority += max(delta.days - task['frequency'], 0)

            if task.get('postponed') is not None:
                if task['postponed']:
                    priority -= 1

            if priority > highest_priority:
                highest_priority = priority
                highest_task = task

        # debug
        print(highest_priority)

        return highest_task


if __name__ == "__main__":
    client = pymongo.MongoClient('192.168.100.108', 27017)
    db = client['test_db']
    task_collection = db.task_list
    done_collection = db.done_list

    finder = TaskFinder(task_collection, done_collection)

    print(finder.next(datetime.datetime.now()))
