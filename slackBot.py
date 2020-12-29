from decouple import config
import requests


def send_slack_message(message):
    requests.post(url="https://slack.com/api/chat.postMessage",
                  data={'token': config('SLACK_TOKEN'),
                        "channel": '#content',
                        'text': message})
