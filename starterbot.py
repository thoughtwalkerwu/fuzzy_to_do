# coding: utf-8

import os
import re
import time
import datetime
from slackclient import SlackClient
import pymongo


from constants import BUTTON_JSON
from task_finder import TaskManager
from util import is_int, parse_command

RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


class TaskBot:

    def __init__(self, slack_token, db_url, task_manager: TaskManager):
        print("token: {}".format(slack_token))
        print("db url: {}".format(db_url))
        self.slack_client = SlackClient(slack_token)
        self.starterbot_id = None
        self.im_channel_id = None

        client = pymongo.MongoClient(db_url, 27017)
        db = client['test_db']
        self.task_collection = db.task_list
        self.done_collection = db.done_list

        self.task_manager = task_manager
        print("current_position: {}".format(self.task_manager.position))
        self.displayed_task = None

    def parse_bot_command(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        print(slack_events)
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                if event["channel"] == self.im_channel_id:
                    return event["text"], event["channel"]
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.starterbot_id:
                    return message, event["channel"]
        return None, None

    def parse_direct_mention(self, message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def show_next(self):
        self.displayed_task = self.task_manager.next(datetime.datetime.now())
        return  self.displayed_task.description

    #def done_task(self, task_name):



    def handle_command(self, command: str, channel, condition=None):
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Not sure what you mean."

        # Finds and executes the given command, filling in response
        response = ""

        # Default timestamp
        timestamp = datetime.datetime.now()

        # This is where you start to implement more commands!
        # for handler in task_handlers:
        #     if command.startswith(handler.TASK_COMMAND):
        #         handler.handle_request(command, condition)
        if command.startswith("next"):
            response = "next task is {}.".format(self.show_next())

        elif command.startswith("done"):
            commands = command.split(' ')
            if len(commands) > 1:
                if is_int(commands[1]):
                    try:
                        target_task = self.task_manager.get_task_by_index(int(commands[1]))
                        response = "{} is done! Well done!\n".format(target_task.description)
                        self.task_manager.done_task(target_task, timestamp)
                        self.task_manager.update_task_list()
                        response += self.show_next()
                    except ValueError as e:
                        response = e.args[0]

                else:
                    try:
                        self.task_manager.done_task_by_name(commands[1], timestamp)
                        self.task_manager.update_task_list()
                        response = "{} is done! Well done!\n".format(commands[1])
                        response += self.show_next()
                    except ValueError as e:
                        response = e.args[0]
            else:
                self.task_manager.done_task_by_index(0, timestamp)
                self.task_manager.update_task_list()
                response = "{} is done! Well done!\n".format(self.displayed_task.description)
                response += self.show_next()

        elif command.startswith("postpone"):
            self.task_manager.postpone(self.displayed_task)
            response = "postponed {}.\n".format(self.displayed_task.description)
            response += self.show_next()

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
                    self.task_manager.insert_generator(gen)
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
            tasks = self.task_manager.top(length)
            response = "task list:\n"
            for index, task in enumerate(tasks):
                response += "{} {}: {}, {}\n".format(index, task.description, task.priority, task.due.date())

        elif command.startswith("task"):
            print(command)
            dummy, args = parse_command(['task'], command)
            print(args)
            self.task_manager.add_task(args[0])

        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response#,
            # attachments=BUTTON_JSON['attachments']
        )

    def handle_command_test(self, command_line: str, channel, condition=None):
        """
            Executes bot command if the command is known
        """
        default_response = "Not sure what you mean."

        # Finds and executes the given command, filling in response
        response = ""

        # Default timestamp
        timestamp = datetime.datetime.now()

        # This is where you start to implement more commands!
        # for handler in task_handlers:
        #     if command.startswith(handler.TASK_COMMAND):
        #         handler.handle_request(command, condition)
        command_set = {'next': self.show_next,
                       'done': self.done_task ,
                       }
        command, arg = parse_command(command_set.keys(), command_line)


        if command.startswith("next"):
            response = "next task is {}.".format(self.show_next())

        elif command.startswith("done"):
            commands = command.split(' ')
            if len(commands) > 1:
                if is_int(commands[1]):
                    try:
                        self.task_manager.done_task_by_index(int(commands[1]), timestamp)
                        self.task_manager.update_task_list()
                        response = "{} is done! Well done!\n".format(self.task_manager.get_task_by_index(int(commands[1])).description)
                        response += self.show_next()
                    except ValueError as e:
                        response = e.args[0]

                else:
                    try:
                        self.task_manager.done_task_by_name(commands[1], timestamp)
                        self.task_manager.update_task_list()
                        response = "{} is done! Well done!\n".format(commands[1])
                        response += self.show_next()
                    except ValueError as e:
                        response = e.args[0]
            else:
                self.task_manager.done_task_by_index(0, timestamp)
                self.task_manager.update_task_list()
                response = "{} is done! Well done!\n".format(self.displayed_task.description)
                response += self.show_next()

        elif command.startswith("postpone"):
            self.task_manager.postpone(self.displayed_task)
            response = "postponed {}.\n".format(self.displayed_task.description)
            response += self.show_next()

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
                    self.task_manager.insert_generator(gen)
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
            tasks = self.task_manager.top(length)
            response = "task list:\n"
            for index, task in enumerate(tasks):
                response += "{} {}: {}\n".format(index, task.description, task.priority)

        elif command.startswith("task"):
            print(command)
            dummy, args = parse_command(['task'], command)
            print(args)
            self.task_manager.add_task(args[0])


    def run(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Starter Bot connected and running!")
            self.starterbot_id = self.slack_client.api_call("auth.test")["user_id"]
            self.im_channel_id = self.slack_client.api_call("im.list")["ims"][1]["id"]
            while True:
                raw_command, channel = self.parse_bot_command(self.slack_client.rtm_read())
                if raw_command:
                    self.handle_command(raw_command, channel)
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

        else:
            print("Connection failed. Exception traceback printed above.")


if __name__ == "__main__":

    def parse_line(line: str):
        splits = line.split('=')
        if len(splits) == 2:
            var_name = splits[0]
            value = splits[1]
            return var_name, value
        else:
            return None, None

    import os
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(base, 'bot_settings.config'))
    with open(path) as f:
        for line in f:
            name, v = parse_line(line.rstrip('\n'))
            if name == "slack_token":
                token = v
            elif name == "db_url":
                url = v

    try:
        taskm = TaskManager(url, position="home")
        bot = TaskBot(token, url, taskm)
        bot.run()
    except ConnectionResetError as err:
        print(err)
        print("Connection failed. Exception traceback printed above.")