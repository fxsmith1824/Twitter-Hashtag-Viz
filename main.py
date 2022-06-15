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

translate_punctuation = str.maketrans('','','!.,')

client = tweepy.Client(BEARER_TOKEN)

tweets = client.search_recent_tweets(query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', tweet_fields=['text'], max_results=10)

# Get a list of all the text from tweets
tweet_text = [x.text for x in tweets.data]

words = []

# Clean up the text in each tweet (preliminary - remove links, hashtags, @users, punctuation)
for tweet in tweet_text:
    word_list = tweet.split(' ')
    word_list = [x for x in word_list if not x.startswith('#') and not x.startswith('http') and not x.startswith('@')]
    word_list = [x.translate(translate_punctuation) for x in word_list]
    words += word_list

