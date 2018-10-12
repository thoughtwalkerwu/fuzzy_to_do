import datetime
import pymongo
from util import db_url

from task_generators import TaskGenerator, parse_task_generator, parse_task_generator_list

# client = pymongo.MongoClient(db_url, 27017)
# db = client['test_db']
# task_generator_collection = db.gen_list
# task_generator = TaskGenerator(**task_generator_collection.find())
#


def task_exist(task_name):
    client = pymongo.MongoClient(db_url, 27017)
    db = client['test_db']
    task_collection = db.task_list

    data = task_collection.find_one({'description': task_name})

    if data is not None:
        return True
    else:
        return False


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
        task_collection.insert_one(generator.generate_task(datetime.datetime.now()).to_db_obj())


def done_task_by_name(task_name, time: datetime.datetime):
    client = pymongo.MongoClient(db_url, 27017)
    db = client['test_db']
    task_generator_collection = db.gen_list
    task_collection = db.task_list

    # task_generator = TaskGenerator(**task_generator_collection.find())
    query = {'task.description': task_name}
    print(task_name)
    data = task_generator_collection.find_one(query)
    print(data)
    generator = parse_task_generator(**data)
    if generator.last_done < time:
        task_generator_collection.update(query, {'$set': {'last_done': time}})
        task_collection.delete_one({'description': task_name})
        task_collection.insert_one(generator.generate_task(datetime.datetime.now()).to_db_obj())


def insert_generator(task_json):
    client = pymongo.MongoClient(db_url, 27017)
    db = client['test_db']
    task_generator_collection = db.gen_list
    try:
        task_generator = parse_task_generator(**task_json)
        task_generator_collection.insert_one(task_generator.to_db_obj())
    except:
        raise AttributeError


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


def fill_unadded_tasks(time: datetime.datetime):
    from task import parse_task
    client = pymongo.MongoClient(db_url, 27017)
    db = client['test_db']
    task_generator_collection = db.gen_list
    task_collection = db.task_list

    # task_generator = TaskGenerator(**task_generator_collection.find())
    datas = task_generator_collection.find()

    for data in datas:
        task_gen = parse_task_generator(**data)
        task_data = task_collection.find_one({'description': data['task']['description']})

        if task_data is None:
            print(data['task']['description'])
            task_collection.insert_one(task_gen.generate_task(datetime.datetime.now()).to_db_obj())
