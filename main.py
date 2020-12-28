from datetime import datetime
from threading import Thread
import time
import traceback

import slackBot


def send_time_message():
    current_date = datetime.now()
    current_date_str = current_date.strftime("%c")
    slackBot.send_slack_message(current_date_str)


def send_hourly_msg():
    while True:
        send_time_message()
        time.sleep(3)


def menu():
    while True:
        command = input('''
Please select an option:
[1] Send Now
[2] New Content
[3] Quit
>> ''')

        try:
            if command.lower() == 'quit' or command.lower() == 'q' or int(command) == 3:
                global stop_thread
                stop_thread = True
                print('\nThank you and good bye')
                break
            elif int(command) == 1:
                send_time_message()
            elif int(command) == 2:
               continue
            elif 0 <= int(command) or int(command) > 2:
                raise ValueError
        except ValueError:
            print('Invalid entry, please select valid number from the list of options')
        except Exception:
            traceback.print_exc()


def main():
    send_hourly_msg_thread = Thread(target=send_hourly_msg)
    # We set it as a daemon thread, so you can let them run and forget about it, and when your program quits,
    # any daemon threads are killed automatically.
    send_hourly_msg_thread.daemon = True
    send_hourly_msg_thread.start()
    menu()


if __name__ == '__main__':
    main()
