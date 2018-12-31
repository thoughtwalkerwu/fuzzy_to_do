# coding: utf-8

import datetime
import pymongo
import os

if __name__ == '__main__':
    def parse_line(line: str):
        splits = line.split('=')
        if len(splits) == 2:
            var_name = splits[0]
            value = splits[1]
            return var_name, value
        else:
            return None, None
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(base, 'bot_settings.config'))
    with open(path) as f:
        for line in f:
            name, v = parse_line(line.rstrip('\n'))
            if name == "slack_token":
                token = v
            elif name == "db_url":
                url = v
    client = pymongo.MongoClient(url, 27017)
    print(url)
    db = client['test_db']
    collection = db.gen_list
    for data in collection.find():
        query = {'description': data['description']}

        collection.update_one(query, {'$unset': {'inserted_time': 1}})

    # collection = db.gen_list
    # for data in collection.find():
    #     print(data)