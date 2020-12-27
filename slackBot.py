import slack
from decouple import config

client = slack.WebClient(token=config('SLACK_TOKEN'))
client.chat_postMessage(channel='#content', text="new test")