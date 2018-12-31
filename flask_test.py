import datetime
from flask import Flask, render_template, request
from wtforms.fields.html5 import DateField
from task_finder import TaskManager
from task import Task
app = Flask(__name__)


@app.route('/')
def hello():
    html = render_template(
        "add_task.html",
        render_day="{0:%Y-%m-%d}".format(datetime.datetime.now())
    )
    return html


@app.route('/task_list', methods=['GET', 'POST'])
def show_tasks():
    url = "192.168.100.111"
    taskm = TaskManager(url, position="home")
    head_message = ""
    if request.method == "POST":
        if request.form["submit"] == "DONE":
            taskm.done_task_by_name(request.form["done_task"], time=datetime.datetime.now())
            head_message = "task {} is done! well done!".format(request.form["done_task"])

        elif request.form["submit"] == "ADD":
            due = datetime.datetime.strptime(
                "{} {}".format(
                    request.form["due_date"],
                    request.form["due_time"]
                ),
                '%Y-%m-%d %H:%M'
            )
            task = Task(
                description=request.form["description"],
                inserted_time=datetime.datetime.now(),
                priority=int(request.form["priority"]),
                due=due,
                time_needed=int(request.form["time_needed"])
            )
            taskm.add_task(task)
            head_message = "Added task: {}".format(request.form["description"])
    taskm.update_task_list(True)
    task_list = taskm.top(100)
    html = render_template("task_list.html", tasks=[x.to_db_obj() for x in task_list], head_message=head_message)
    return html


if __name__ == "__main__":
    app.run(debug=True)
