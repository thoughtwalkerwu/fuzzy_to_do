import datetime
import pprint
from frequent_task import UnscheduledTaskGen, WeeklyTaskGen, TaskTemplate
from task import Task

# tasks = [
#     UnscheduledTaskGen(Task("洗濯",                  "home","any",4,15,False,datetime.date(2018,9,10)),frequency=2),
#     UnscheduledTaskGen(Task("ルンバ起動",            "home","any",4,15,False,datetime.date(2018,9,10)),frequency=3),
#     UnscheduledTaskGen(Task("食器洗い",              "home","any",4,15,False,datetime.date(2018,9,10)),frequency=3),
#     UnscheduledTaskGen(Task("洗面タオル入れ替え",    "home","any",4,15,False,datetime.date(2018,9,10)),frequency=10),
#     UnscheduledTaskGen(Task("棚・テーブル拭き",      "home","any",4,15,False,datetime.date(2018,9,10)),frequency=10),
#     UnscheduledTaskGen(Task("シンクネット取り換え",  "home","any",4,15,False,datetime.date(2018,9,10)),frequency=7),
#     UnscheduledTaskGen(Task("トイレ掃除",            "home","any",4,15,False,datetime.date(2018,9,10)),frequency=5),
#     UnscheduledTaskGen(Task("風呂掃除",              "home","any",4,15,False,datetime.date(2018,9,10)),frequency=10),
#     UnscheduledTaskGen(Task("朝食",                  "home","any",4,15,False,datetime.date(2018,9,10)),frequency=1),
#     UnscheduledTaskGen(Task("着替え",                "home","any",4,15,False,datetime.date(2018,9,10)),frequency=1),
#     UnscheduledTaskGen(Task("靴下探し",              "home","any",4,15,False,datetime.date(2018,9,10)),frequency=1),
#     UnscheduledTaskGen(Task("スーツ着る",            "home","any",4,15,False,datetime.date(2018,9,10)),frequency=1),
#     UnscheduledTaskGen(Task("ベルトつける",          "home","any",4,15,False,datetime.date(2018,9,10)),frequency=1),
#     UnscheduledTaskGen(Task("荷物確認",              "home","any",4,15,False,datetime.date(2018,9,10)),frequency=1),
# ]
tasks = [
    {'last_done': datetime.date(2018, 1, 1), 'frequency': 2, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '洗濯', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 3, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': 'ルンバ起動', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 3, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '食器洗い', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 10, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '洗面タオル入れ替え', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 10, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '棚・テーブル拭き', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 7, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': 'シンクネット取り換え', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 5, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': 'トイレ掃除', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 10, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '風呂掃除', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 1, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '朝食', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 1, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '着替え', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 1, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '靴下探し', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 1, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': 'スーツ着る', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 1, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': 'ベルトつける', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
    ,{'last_done': datetime.date(2018, 1, 1), 'frequency': 1, 'task': {'priority': 4, 'due': datetime.date(2018, 1, 3), 'time_needed': 15, 'description': '荷物確認', 'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
]

for gen in tasks:
    generator = UnscheduledTaskGen(**gen)
    pprint.pprint(generator.to_db_obj())
