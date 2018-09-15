# coding: utf-8

import pymongo

from util import db_url

if __name__ == '__main__':
    client = pymongo.MongoClient(db_url, 27017)
    print(db_url)
    db = client['test_db']
    collection = db.task_list
    for data in collection.find():
        print(data)

    # collection = db.gen_list
    # for data in collection.find():
    #     print(data)