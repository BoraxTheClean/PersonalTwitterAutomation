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
    favorites = ['StarGazerNumber','shoop_hs','xfileMTG','VTCLA1','Bloody','Grischa_','TenaciousMTG','yoman_5','Nafiusx','joemag_games','bertuuu','lucasfaley','misplacedginger','KanyeBestMTG','AlphaPhrog','SamRolph3','Whoot1234','olivia_claire_','realjoepatry','NetRepTodd','dillyg10','Rage_HS','HS_Orange']
    clear_timeline()
    favorite_tweets(favorites)

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
        print('Inspecting tweets from: '+user_id)
        try:
            for status in tweepy.Cursor(api.user_timeline,screen_name=user_id).items(30):
                print(status.text)
                print(status.favorited)
                if not status.favorited:
                    favorite_status(status)
        except:
            print("Error trying to retrieve tweets. Perhaps a name change?")

def destroy_status(id):
    api.destroy_status(id)

def favorite_status(status):
    status.favorite()
