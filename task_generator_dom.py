import datetime
import pymongo
from util import db_url

from task_generators import TaskGenerator, parse_task_generator, parse_task_generator_list

# client = pymongo.MongoClient(db_url, 27017)
# db = client['test_db']
# task_generator_collection = db.gen_list
# task_generator = TaskGenerator(**task_generator_collection.find())
#


def done_task(task, time: datetime.datetime):
    client = pymongo.MongoClient(db_url, 27017)
    db = client['test_db']
    task_generator_collection = db.gen_list
    task_collection = db.task_list

    # task_generator = TaskGenerator(**task_generator_collection.find())
    query = {'task.description': task.description}
    print(task.description)
    data = task_generator_collection.find_one(query)
    print(data)
    generator = parse_task_generator(**data)
    if generator.last_done < time:
        task_generator_collection.update(query, {'$set': {'last_done': time}})
        task_collection.delete_one({'description': task.description})


def dump_task_generators():
    client = pymongo.MongoClient(db_url, 27017)
    db = client['test_db']
    task_generator_collection = db.gen_list
    task_generator = TaskGenerator(parse_task_generator_list(task_generator_collection.find()))
    return task_generator.to_db_obj()


def dump_tasks():
    client = pymongo.MongoClient(db_url, 27017)
    db = client['test_db']
    task_collection = db.task_list
    return task_collection.find()