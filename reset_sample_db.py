# coding: utf-8


import datetime
import pymongo

from frequent_task import UnscheduledTaskGen, WeeklyTaskGen, TaskTemplate
from util import db_url

client = pymongo.MongoClient(db_url, 27017)
db = client['test_db']
task_collection = db.task_list
task_generator_collection = db.gen_list

# morning_obj = MorningTask(task_collection, datetime.time(21, 0, 0))
# # daily_obj = TaskBase(task_collection)
# task_handlers = {morning_obj, daily_obj}

task_collection.delete_many({'position':"any"})
task_collection.delete_many({'position':"home"})

task_generator_collection.delete_many({'position':"home"})
task_generator_collection.delete_many({'task_type': 'Unscheduled'})


tasks = [
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 2,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15,
              'description': 'モゴモゴバスター', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 2,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '筋肉体操',
              'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 2,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15,
              'description': 'タイピング練習', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 2,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '洗濯',
              'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 3,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': 'ルンバ起動',
              'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 3,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '食器洗い',
              'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 10,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15,
              'description': '洗面タオル入れ替え', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 10,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15,
              'description': '棚・テーブル拭き', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 7,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15,
              'description': 'シンクネット取り換え', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 5,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': 'トイレ掃除',
              'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 10,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '風呂掃除',
              'time_slot': 'any', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 1,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '朝食',
              'time_slot': 'morning', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 1,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '着替え',
              'time_slot': 'morning', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 1,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '靴下探し',
              'time_slot': 'morning', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 1,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': 'スーツ着る',
              'time_slot': 'morning', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 1,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15,
              'description': 'ベルトつける', 'time_slot': 'morning', 'cancellable': False, 'position': 'home'}},
    {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 1, 1, 10, 0, 0), 'frequency': 1,
     'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15, 'description': '荷物確認',
              'time_slot': 'morning', 'cancellable': False, 'position': 'home'}},

]

for gen in tasks:
    generator = UnscheduledTaskGen(**gen)
    print(generator.to_db_obj())
    task_generator_collection.insert_one(generator.to_db_obj())

for data in task_generator_collection.find():
    print(data)
    generator = UnscheduledTaskGen(**data)
    task = generator.generate_task(datetime.datetime.now()).to_db_obj()
    print(task)
    task_collection.insert_one(task)
