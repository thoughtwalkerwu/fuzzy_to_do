# coding: utf-8

import pymongo
import datetime
from task import parse_task, Task
from util import db_url

if __name__ == '__main__':
    client = pymongo.MongoClient(db_url, 27017)
    print(db_url)
    db = client['test_db']
    collection = db.task_list
    for data in collection.find():
        task = parse_task(**data)
        print("task: {}, priority: {}".format(
            task.description,
            task.get_priority(datetime.datetime.now(), "home", "any"))
        )