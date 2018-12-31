import datetime

from frequent_task import UnscheduledTaskGen, WeeklyTaskGen, TaskTemplate, Task


def parse_task_generator_list(gen_json_list):
    gen_list = []
    for gen_db_obj in gen_json_list:
        print(gen_db_obj)
        gen_list.append(parse_task_generator(**gen_db_obj))

    return gen_list


def parse_task_generator(**kwargs):
    task_type = kwargs['task_type']

    if task_type == "Unscheduled":
        return UnscheduledTaskGen(**kwargs)
    elif task_type == "Weekly":
        return WeeklyTaskGen(**kwargs)

class TaskGenerator:
    def __init__(self, task_generators: list):
        self.task_generators = task_generators

    def generate_tasks(self, time: datetime.datetime):
        tasks = []
        for generator in self.task_generators:
            task = generator.generate_task(time)
            if task is not None:
                tasks.append(task)
        return tasks

    def to_db_obj(self):
        db_obj = {}
        for gen in self.task_generators:
            db_obj[gen.description] = gen.to_db_obj()

