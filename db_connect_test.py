# coding: utf-8

import pymongo


if __name__ == '__main__':
    client = pymongo.MongoClient('192.168.100.108', 27017)

    db = client['test_db']
    collection = db.task_list
    for data in collection.find():
        print(data)
        if data["description"].startswith("morning"):
            collection.remove({"description": data["description"]})


