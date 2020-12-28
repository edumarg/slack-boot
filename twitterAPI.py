from decouple import config
import tweepy

twitter_users = ['PythonWeekly', 'realpython', 'fullstackpython']

# tewttpy documentation at http://docs.tweepy.org/en/latest/api.html

auth = tweepy.OAuthHandler(config("consumer_key"), config("consumer_secret"))
auth.set_access_token(config("access_token"), config("access_token_secret"))

api = tweepy.API(auth)