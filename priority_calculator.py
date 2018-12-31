import datetime


class PriorityCalculator:
    def __init__(self):
        self.position_weight = 3

        def urgency_function(time_remain: float, whole_time: float):
            return 1 - time_remain/whole_time
        self.urgency_function = urgency_function

    def calc_priority(self, task, time: datetime.datetime, position: str='any'):
        base_priority = task.priority

        whole_time = (task.due - task.inserted_time).total_seconds()
        time_remain = max((task.due - time).total_seconds(), 0)

        accrual = self.urgency_function(time_remain, whole_time)

        if task.position == position:
            base_priority += self.position_weight
        elif task.position != 'any':
            print(task.position)
            return 0

        return accrual * base_priority


