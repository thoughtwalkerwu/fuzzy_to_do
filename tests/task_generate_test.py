import datetime
import pymongo
from util import db_url
from frequent_task import UnscheduledTaskGen, WeeklyTaskGen, TaskTemplate

from task_generators import TaskGenerator, parse_task_generator
from task_generator_dom import done_task, dump_task_generators, dump_tasks

print(dump_tasks())
print(dump_task_generators())

# done_task(tasks[3], datetime.datetime.now())

