from datetime import datetime
from threading import Thread
import time
import traceback

import slackBot
import twitterAPI


def send_time_message():
    current_date = datetime.now()
    current_date_str = current_date.strftime("%c")
    slackBot.send_slack_message(current_date_str)


def send_hourly_msg():
    while True:
        send_time_message()
        time.sleep(3600)


def send_tweet(tweets):
    for tweet in tweets:
        slackBot.send_slack_message(tweet)


def send_new_content():
    tweets = twitterAPI.get_new_content()
    send_tweet(tweets)


def send_my_new_content():
    while True:
        tweets = twitterAPI.get_my_new_tweets()
        send_tweet(tweets)
        time.sleep(600)


def menu():
    while True:
        command = input('''
Please select an option:
[1] Send Now
[2] New Content
[3] tweet
[4] Quit
>> ''')

        try:
            if command.lower() == 'quit' or command.lower() == 'q' or int(command) == 4:
                print('Thank you and good bye')
                break
            elif int(command) == 1:
                send_time_message()
            elif int(command) == 2:
                send_new_content()
            elif int(command) == 3:
                message = input('''Type message to tweet: 
                >>>''')
                if len(message) > 280:
                    print("Maximum characters for a message is 280")
                elif len(message) == 0:
                    print("Message cannot be empty")
                else:
                    twitterAPI.send_tweet(message)
            elif 0 <= int(command) or int(command) > 3:
                raise ValueError
        except ValueError:
            print('Invalid entry, please select valid number from the list of options')
        except Exception:
            traceback.print_exc()


def main():
    send_hourly_msg_thread = Thread(target=send_hourly_msg)
    send_hourly_msg_thread.start()
    check_my_tweets_thread = Thread(target=send_my_new_content)
    check_my_tweets_thread.start()

    menu()


if __name__ == '__main__':
    main()
