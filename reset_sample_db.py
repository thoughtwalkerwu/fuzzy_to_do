# coding: utf-8


import datetime
import pymongo

from task_generators import MorningTask, TaskBase


client = pymongo.MongoClient('192.168.100.111', 27017)
db = client['test_db']
task_collection = db.task_list
done_collection = db.done_list

morning_obj = MorningTask(task_collection, datetime.time(21, 0, 0))
daily_obj = TaskBase(task_collection)
task_handlers = {morning_obj, daily_obj}

task_collection.delete_many({'position': "home"})

daily_obj.add_task(
        description="洗濯",
        time_slot="any",
        frequency=2,
        cancellable=False,
        position="home",
        grouping=None,
        priority=4,
        time_needed=15,
        
)

daily_obj.add_task(

            description="ルンバ起動",
            time_slot="any",
            frequency=2,
            cancellable=False,
            position="home",
            grouping=None,
            priority=4,
            time_needed=15,
            

)

daily_obj.add_task(

            description="食器洗い",
            time_slot="any",
            frequency=3,
            cancellable=False,
            position="home",
            grouping=None,
            priority=4,
            time_needed=15,
            

)

daily_obj.add_task(

            description="洗面タオル入れ替え",
            time_slot="any",
            frequency=10,
            cancellable=False,
            position="home",
            grouping=None,
            priority=4,
            time_needed=5,
            

)

daily_obj.add_task(

            description="棚・テーブル拭き",
            time_slot="any",
            frequency=7,
            cancellable=False,
            position="home",
            grouping=None,
            priority=4,
            time_needed=15,
            

)


daily_obj.add_task(

            description="シンクネット取り換え",
            time_slot="any",
            frequency=7,
            cancellable=False,
            position="home",
            grouping=None,
            priority=4,
            time_needed=15,
            

)


daily_obj.add_task(

            description="トイレ掃除",
            time_slot="any",
            frequency=7,
            cancellable=False,
            position="home",
            grouping=None,
            priority=4,
            time_needed=15,
            

)
daily_obj.add_task(
            description="風呂掃除",
            time_slot="any",
            frequency=12,
            cancellable=False,
            position="home",
            grouping=None,
            priority=4,
            time_needed=15,
)


daily_obj.add_task(
            description="朝食",
            time_slot="morning",
            frequency=1,
            cancellable=False,
            position="home",
            before=8,
            grouping=None,
            priority=4,
            time_needed=15,
)


daily_obj.add_task(
            description="着替え",
            time_slot="morning",
            frequency=1,
            cancellable=False,
            position="home",
            before=8,
            grouping=None,
            priority=4,
            time_needed=15,
)

daily_obj.add_task(
            description="靴下探し",
            time_slot="morning",
            frequency=1,
            cancellable=False,
            position="home",
            before=8,
            grouping=None,
            priority=4,
            time_needed=3,
)
daily_obj.add_task(
            description="スーツ着る",
            time_slot="morning",
            frequency=1,
            cancellable=False,
            position="home",
            before=8,
            grouping=None,
            priority=4,
            time_needed=5,
)

daily_obj.add_task(
            description="ベルトつける",
            time_slot="morning",
            frequency=1,
            cancellable=False,
            position="home",
            before=8,
            grouping=None,
            priority=4,
            time_needed=2,
)


daily_obj.add_task(
            description="荷物確認",
            time_slot="morning",
            frequency=1,
            cancellable=False,
            position="home",
            before=8,
            grouping=None,
            priority=4,
            time_needed=2,
)