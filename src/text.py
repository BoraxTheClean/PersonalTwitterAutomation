import os
import tweepy
import boto3
import datetime

ssm = boto3.client('ssm')

try:
    CONSUMER_KEY = ssm.get_parameter(Name='/personal/CONSUMER_KEY',WithDecryption=True)['Parameter']['Value'].strip()
    CONSUMER_SECRET = ssm.get_parameter(Name='/personal/CONSUMER_SECRET',WithDecryption=True)['Parameter']['Value'].strip()
    ACCESS_TOKEN = ssm.get_parameter(Name='/personal/ACCESS_TOKEN',WithDecryption=True)['Parameter']['Value'].strip()
    ACCESS_SECRET = ssm.get_parameter(Name='/personal/ACCESS_SECRET',WithDecryption=True)['Parameter']['Value'].strip()
except Exception as error:
    print(error)
    print("Failed to fetch api keys.")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
user = api.me()
print('Tweeting for '+user.name)
def handler(event, context):
    #Users that recieve perpetual likes.
    FAVORITE_PEOPLE = os.environ.get('FAVORITE_PEOPLE').split(',')
    clear_timeline()
    favorite_tweets(FAVORITE_PEOPLE)

#Deletes tweets older than a week.
def clear_timeline():
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(weeks=1)
    for status in tweepy.Cursor(api.user_timeline).items():
        if status.created_at < last_week:
            destroy_status(status.id)

#Like the last 30 tweets from each of my favorite users.
def favorite_tweets(user_ids):
    for user_id in user_ids:
        try:
            for status in tweepy.Cursor(api.user_timeline,screen_name=user_id).items(30):
                if not status.favorited:
                    favorite_status(status)
        except Exception as e:
            print(e)
        finally:
            print("Error trying to retrieve tweets. Perhaps a name change? Name: "+user_id)

def destroy_status(id):
    api.destroy_status(id)

def favorite_status(status):
    status.favorite()
