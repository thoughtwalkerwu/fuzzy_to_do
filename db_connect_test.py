# coding: utf-8

import pymongo
import os

db_url = os.environ.get('MONGO_URL')

if __name__ == '__main__':
    client = pymongo.MongoClient(db_url, 27017)

    db = client['test_db']
    collection = db.task_list
    for data in collection.find():
        print(data)


