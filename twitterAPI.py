from datetime import datetime
from decouple import config
import pytz
import tweepy
import traceback


twitter_users = ['PythonWeekly', 'realpython', 'fullstackpython']
old_user_tweets = []
old_my_tweets = []


def convert_twitter_date_to_timestamp(date):
    #  convert twitter date to python date from
    #  https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
    return datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y').timestamp()


def convert_current_time_to_timestamp(time_zone):
    return datetime.now(pytz.timezone(time_zone)).timestamp()


# tweepy documentation at http://docs.tweepy.org/en/latest/api.html
auth = tweepy.OAuthHandler(config("consumer_key"), config("consumer_secret"))
auth.set_access_token(config("access_token"), config("access_token_secret"))

api = tweepy.API(auth)


def get_new_tweets(user_tweets, twitter_user, old_tweets):
    user_new_tweets = []
    for tweet in user_tweets:
        # New tweets are considered as all tweets from last hour
        if (convert_current_time_to_timestamp("israel") >= convert_twitter_date_to_timestamp(tweet.created_at) >= (
                convert_current_time_to_timestamp("israel") - (3600 * 1000))) and tweet.id not in old_tweets:
            user_new_tweet = f'{tweet.text} \n https://twitter.com/{twitter_user}/status/{tweet.id}'
            user_new_tweets.append(user_new_tweet)
            old_tweets = []
            old_tweets += user_new_tweets
    return user_new_tweets


def get_my_new_tweets():
    my_tweets = api.home_timeline()
    return get_new_tweets(my_tweets, config('my_twitter_user'), old_my_tweets)


def get_user_new_tweets(twitter_user):
    user_tweets = api.user_timeline(screen_name=twitter_user)
    return get_new_tweets(user_tweets, twitter_user, old_user_tweets)
    # for tweet in user_tweets:
    #     # New tweets are considered as all tweets from last hour
    #     if convert_current_time_to_timestamp("israel") >= convert_twitter_date_to_timestamp(tweet.created_at) >= (
    #             convert_current_time_to_timestamp("israel") - (3600 * 1000)):
    #         user_new_tweet = f'{tweet.text} \n https://twitter.com/{twitter_user}/status/{tweet.id}'
    #         user_new_tweets.append(user_new_tweet)
    # return user_new_tweets


def get_new_content():
    new_content = []
    try:
        for user in twitter_users:
            user_new_tweets = get_user_new_tweets(user)
            new_content += user_new_tweets
        return new_content
    except tweepy.TweepError:
        traceback.print_exc()


def send_tweet(message):
    api.update_status(status=message)