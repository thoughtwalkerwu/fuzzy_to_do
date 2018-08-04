# coding: utf-8

import os
import time
import re
import datetime
from slackclient import SlackClient
import pymongo

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None
im_channel_id = None

client = pymongo.MongoClient('localhost', 27017)
db = client['test_db']
collection = db.task_list

RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "do"
MORNING_TASK_COMMAND = "morning"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def add_morning_task(description):
    post = {
        "description": description,
        "time_slot": "morning",
        "frequency": "everyday",
        "priority": "5"
    }
    collection.insert_one(post)


def morning_now():
    morning_hour = 22 
    morning_minute = 0 

    now = datetime.datetime.now()
    print(now.minute == morning_minute)
    print(now.second == 0)
    if morning_hour == now.hour and morning_minute == now.minute and now.second == 0:
        print("morning now")
        return True 


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


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = u""
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    if command == MORNING_TASK_COMMAND:
        response += u"朝のタスク一覧\n"
        for task in collection.find({"time_slot": "morning"}):
            response += task["description"] + u"\n"
    elif command.startswith(MORNING_TASK_COMMAND):
        task_name = re.sub(MORNING_TASK_COMMAND + " ", "", command)
        add_morning_task(task_name)
        print(task_name)
        response += task_name + "is added"
 
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        im_channel_id = slack_client.api_call("im.list")["ims"][1]["id"]
        while True:
            command, channel = parse_bot_command(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            # morning_tasks
            if morning_now():
                tasks = collection.find({"time_slot": "morning"})
                task_list=u"Good morning! let's begin moving!\n" 
                for task in tasks:
                    task_list += u"{}\n".format(task["description"]) 
                # Sends the response back to the channel
                slack_client.api_call(
                "chat.postMessage",
                channel=im_channel_id,
                text=task_list
                )

            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

