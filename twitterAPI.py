from datetime import datetime, timezone
from decouple import config
import pytz
import tweepy

old_user_tweets = []
old_my_tweets = []

# tweepy documentation at http://docs.tweepy.org/en/latest/api.html
auth = tweepy.OAuthHandler(config("consumer_key"), config("consumer_secret"))
auth.set_access_token(config("access_token"), config("access_token_secret"))

api = tweepy.API(auth)


def convert_twitter_date_to_timestamp(date):
   # convert utc to loal time
   # https://stackoverflow.com/questions/4563272/convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-standard-lib
    return date.replace(tzinfo=timezone.utc).astimezone(tz=None).timestamp()


def convert_current_time_to_timestamp(time_zone):
    return datetime.now(pytz.timezone(time_zone)).timestamp()


def get_new_tweets(user_tweets, twitter_user, old_tweets):
    user_new_tweets = []
    for tweet in user_tweets:
        # New tweets are considered as all tweets from last hour
        if (convert_current_time_to_timestamp("israel") >= convert_twitter_date_to_timestamp(tweet.created_at) >= (
                convert_current_time_to_timestamp("israel") - 3600)) and tweet.id not in old_tweets:
            user_new_tweet = f'{tweet.text} \n https://twitter.com/{twitter_user}/status/{tweet.id}'
            user_new_tweets.append(user_new_tweet)
            old_tweets.append(tweet.id)
    return user_new_tweets


def get_user_new_tweets(user):
    try:
       user_tweets = api.user_timeline(screen_name=user)
       return get_new_tweets(user_tweets, user, old_user_tweets)
    except tweepy.TweepError:
        pass


def get_new_content(users):
    try:
        new_content = []
        for user in users:
            user_new_tweets = get_user_new_tweets(user)
            new_content += user_new_tweets
        return new_content
    except tweepy.TweepError:
        pass
    except TypeError:
        return None


def send_tweet(message):
    try:
        api.update_status(status=message)
    except tweepy.TweepError:
        pass
