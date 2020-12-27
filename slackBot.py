import slack
from decouple import config

def send_slack_message(message):
    client = slack.WebClient(token=config('SLACK_TOKEN'))
    client.chat_postMessage(channel='#content', text=message)