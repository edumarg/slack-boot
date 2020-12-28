from datetime import datetime
from threading import Thread
import time

import slackBot



def send_hourly_msg():
    while True:
        current_date = datetime.now()
        current_date_str=current_date.strftime("%c")
        slackBot.send_slack_message(current_date_str)
        time.sleep(3)



def main():
    send_hourly_msg_thread = Thread(target = send_hourly_msg())
    send_hourly_msg_thread.start()


if __name__ == '__main__':
    main()