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

api = tweepy.API(auth)
user = api.me()
print('Tweeting for '+user.name)
def handler(event, context):
    clear_timeline()

#Deletes tweets older than a week.
def clear_timeline():
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(weeks=12)
    for i in range(500):
        try:
            tweets = api.user_timeline(page=i)
        except Error as error:
            print(error)
        if len(tweets) == 0:
            return
        for tweet in tweets:
            if tweet.created_at < last_week:
                print("Deleting "+str(tweet.id))
                destroy_status(tweet.id)


def destroy_status(id):
    api.destroy_status(id)
