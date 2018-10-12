# coding: utf-8

import os
import re
import time
import datetime
from slackclient import SlackClient
import pymongo


from constants import BUTTON_JSON
from task_finder import TaskFinder
from util import db_url, slack_token, is_int
from task_generator_dom import done_task, insert_generator, fill_unadded_tasks

token = slack_token
print(token)
slack_client = SlackClient(token)
starterbot_id = None
im_channel_id = None

client = pymongo.MongoClient(db_url, 27017)
db = client['test_db']
task_collection = db.task_list
done_collection = db.done_list

RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

task_finder = TaskFinder(task_collection)
displayed_task = None


def parse_bot_command(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    print(slack_events)
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            if event["channel"] == im_channel_id:
                return event["text"], event["channel"]   
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def show_next():
    global displayed_task
    displayed_task = task_finder.next(datetime.datetime.now())
    return  displayed_task.description


def handle_command(command: str, channel, condition=None):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = ""

    # Default timestamp
    timestamp = datetime.datetime.now()

    # This is where you start to implement more commands!
    # for handler in task_handlers:
    #     if command.startswith(handler.TASK_COMMAND):
    #         handler.handle_request(command, condition)
    if command.startswith("next"):
        response = "next task is {}.".format(show_next())

    elif command.startswith("done"):
        commands = command.split(' ')
        if len(commands) > 1:
            if is_int(commands[1]):
                try:
                    task_finder.done_task_by_index(int(commands[1]), timestamp)
                    task_finder.update_task_list()
                    response = "{} is done! Well done!\n".format(task_finder.get_task_by_index(int(commands[1])))
                    response += show_next()
                except ValueError as e:
                    response = e.args[0]

            else:
                try:
                    task_finder.done_task_by_name(commands[1], timestamp)
                    task_finder.update_task_list()
                    response = "{} is done! Well done!\n".format(commands[1])
                    response += show_next()
                except ValueError as e:
                    response = e.args[0]
        else:
            done_task(displayed_task, timestamp)
            task_finder.update_task_list()
            response = "{} is done! Well done!\n".format(displayed_task.description)
            response += show_next()

    elif command.startswith("postpone"):
        task_finder.postpone(displayed_task)
        response = "postponed {}.\n".format(displayed_task.description)
        response += show_next()

    elif command.startswith("adddaily"):
        commands = command.split(' ')
        if len(commands) > 1:
            if len(commands) > 2 and is_int(commands[2]):
                frequency = int(commands[2])
            else:
                frequency = 5
            gen = {'task_type': 'Unscheduled', 'last_done': datetime.datetime(2018, 9, 16, 12, 30, 0),
                   'frequency': frequency,
             'task': {'priority': 4, 'due': datetime.datetime(2018, 1, 10, 10, 0, 0), 'time_needed': 15,
                      'description': commands[1],
                      'time_slot': 'any', 'cancellable': False, 'position': 'home'}}
            try:
                insert_generator(gen)
                fill_unadded_tasks(datetime.datetime.now())
                response = "A task {} is added!".format(commands[1])

            except:
                response = "Failed to add task. Something wrong!"

    elif command.startswith("top"):
        commands = command.split(' ')
        length = 10
        if len(commands) > 1:
            try:
                length = int(commands[1])
            except ValueError:
                length = 10
        tasks = task_finder.top(length)
        response = "task list:\n"
        for index, task in enumerate(tasks):
            response += "{} {}: {}\n".format(index, task.description, task.priority)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response#,
        # attachments=BUTTON_JSON['attachments']
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        im_channel_id = slack_client.api_call("im.list")["ims"][1]["id"]
        while True:
            try:
                raw_command, channel = parse_bot_command(slack_client.rtm_read())
                if raw_command:
                    handle_command(raw_command, channel)
                # morning_tasks
                # if morning_obj.is_morning(datetime.datetime.now()):
                #     tasks = task_collection.find({"time_slot": "morning"})
                #     task_list = "Good morning! let's begin moving!\n"
                #     for task in tasks:
                #         task_list += u"{}\n".format(task["description"])
                #     # Sends the response back to the channel
                #     slack_client.api_call(
                #         "chat.postMessage",
                #         channel=im_channel_id,
                #         text=task_list,
                #         )

                time.sleep(RTM_READ_DELAY)
            except ConnectionResetError as error:
                print(error)
                pass
    else:
        print("Connection failed. Exception traceback printed above.")

