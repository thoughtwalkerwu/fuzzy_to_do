import os
import sys
from starterbot import TaskBot


def start_bot():
    try:
        bot = TaskBot()
        bot.run()
    except ConnectionResetError as err:
        print(err)
        print("Connection failed. Exception traceback printed above.")


def create_daemon():
    pid = os.fork()

    if pid > 0:
        f2 = open('/var/run/python_daemon.pid', 'w')
        f2.write(str(pid)+"\n")
        f2.close()
        sys.exit()

    if pid == 0:
        i = 0
        start_bot()


if __name__ == '__main__':
    create_daemon()
