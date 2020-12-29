from datetime import datetime
from threading import Thread
import time


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
    if tweets:
        for tweet in tweets:
            slackBot.send_slack_message(tweet)
    else:
        print("There are no new tweets")
        menu()


def send_new_content(twitter_users):
    tweets = twitterAPI.get_new_content(twitter_users)
    send_tweet(tweets)


def send_my_new_content():
    while True:
        tweets = twitterAPI.get_my_new_tweets()
        send_tweet(tweets)
        time.sleep(600.0)


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
                twitter_users = ['PythonWeekly', 'realpython', 'fullstackpython']
                send_new_content(twitter_users)
            elif int(command) == 3:
                message = input('Type message to tweet:\n>>>')
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
        except TypeError:
            print("There are no new Tweets")


def main():
    #  A daemon thread runs without blocking the main program from exiting.
    #  And when main program exits, associated daemon threads are killed too.
    # https://www.journaldev.com/16152/python-daemon-thread
    send_hourly_msg_thread = Thread(target=send_hourly_msg, daemon=True)
    send_hourly_msg_thread.start()
    check_my_tweets_thread = Thread(target=send_my_new_content, daemon=True)
    check_my_tweets_thread.start()
    menu()


if __name__ == '__main__':
    main()
