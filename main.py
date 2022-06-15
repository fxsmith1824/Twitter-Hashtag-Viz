# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:09:34 2022

@author: fxsmith1824
"""

import tweepy
import os
from dotenv import load_dotenv
import wordcloud
import matplotlib.pyplot as plt

load_dotenv()

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

translate_punctuation = str.maketrans('','','!.,')
excluded_phrases = ['GUILDWARS', 'GUILD WARS', 'GUILDWARS2', 'GUILD WARS 2', 'GW2', 'GUILD', 'WARS', '2']
excluded_phrases = [x.casefold() for x in excluded_phrases]

client = tweepy.Client(BEARER_TOKEN)

count = client.get_recent_tweets_count(query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', granularity='day')

tweets = client.search_recent_tweets(query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', tweet_fields=['text'], max_results=100)
# tweets = tweepy.Paginator(client.search_recent_tweets, query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', tweet_fields=['text'], max_results=100).flatten(limit=1000)


# Get a list of all the text from tweets
tweet_text = [x.text for x in tweets.data]

words = []

# Clean up the text in each tweet (preliminary - remove links, hashtags, @users, punctuation)
for tweet in tweet_text:
    word_list = tweet.split(' ')
    word_list = [x for x in word_list if not x.startswith('#') and not x.startswith('http') and not x.startswith('@')]
    word_list = [x for x in word_list if 'http' not in x]
    word_list = [x for x in word_list if '#' not in x]
    word_list = [x for x in word_list if x.casefold() not in excluded_phrases]
    word_list = [x.translate(translate_punctuation) for x in word_list]
    words += word_list

text = ' '.join(words)
cloud = wordcloud.WordCloud(max_words=20).generate(text)

plt.imshow(cloud, interpolation='bilinear')
plt.axes('off')
plt.show()