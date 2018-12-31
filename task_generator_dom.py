import datetime
import pymongo
from task_generators import TaskGenerator, parse_task_generator, parse_task_generator_list
from task import Task, parse_task

# client = pymongo.MongoClient(db_url, 27017)
# db = client['test_db']
# task_generator_collection = db.gen_list
# task_generator = TaskGenerator(**task_generator_collection.find())
#


class TaskReaderDOM:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def find_all(self):
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        task_collection = db.task_list

        return task_collection.find()

    def task_exist(self, task_name):
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        task_collection = db.task_list

        data = task_collection.find_one({'description': task_name})

        if data is not None:
            return True
        else:
            return False

    def dump_task_generators(self):
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        task_generator_collection = db.gen_list
        task_generator = TaskGenerator(parse_task_generator_list(task_generator_collection.find()))
        return task_generator.to_db_obj()

    def dump_tasks(self, ):
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        task_collection = db.task_list
        return task_collection.find()


class TaskWriterDOM(TaskReaderDOM):
    def __init__(self, db_url: str):
        self.db_url = db_url

    def done_task(self, task, time: datetime.datetime):
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        # task_generator_collection = db.gen_list
        task_collection = db.task_list
        task_collection.delete_one({'description': task.description})
        done_collection = db.done_list
        done_collection.insert_one({'task': task.description, 'timestamp': time})

    def insert_task(self, task: Task):
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        task_collection = db.task_list
        try:
            task_collection.insert_one(task.to_db_obj())
        except:
            raise AttributeError

    def insert_generator(self, task_json):
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        task_generator_collection = db.gen_list
        try:
            task_generator = parse_task_generator(**task_json)
            task_generator_collection.insert_one(task_generator.to_db_obj())
        except:
            raise AttributeError

    def fill_unadded_tasks(self, time: datetime.datetime):
        from task import parse_task
        client = pymongo.MongoClient(self.db_url, 27017)
        db = client['test_db']
        task_generator_collection = db.gen_list
        task_collection = db.task_list

        # task_generator = TaskGenerator(**task_generator_collection.find())
        datas = task_generator_collection.find()

        for data in datas:
            data['task']['inserted_time'] = time
            task_gen = parse_task_generator(**data)
            task_data = task_collection.find_one({'description': data['task']['description']})

            if task_data is None:
                print(data['task']['description'])
                task_collection.insert_one(task_gen.generate_task(datetime.datetime.now()).to_db_obj())
