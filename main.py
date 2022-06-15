# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:09:34 2022

@author: fxsmith1824
"""

import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

client = tweepy.Client(BEARER_TOKEN)

tweets = client.search_recent_tweets(query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', tweet_fields=['text'], max_results=10)

for tweet in tweets.data:
    print(tweet.text)