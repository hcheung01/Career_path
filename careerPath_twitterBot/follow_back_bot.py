#!/usr/bin/python3
"""Module for tweep program"""


# Python library for accessing the Twitter API
import tweepy

# Import our Twitter credentials from credentials.py
from credentials import *

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Connection test
# Connection test
user = api.me()
print (user.name)

# Follow everyone following
for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
    print("Followed everyone that is following " + user.name)

