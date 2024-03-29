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
from datetime import date

load_dotenv()

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

translate_punctuation = str.maketrans('','','!.,')
excluded_phrases = ['GUILDWARS', 'GUILD WARS', 'GUILDWARS2', 'GUILD WARS 2', 'GW2', 'GUILD', 'WARS', '2']
excluded_phrases = [x.casefold() for x in excluded_phrases]

client = tweepy.Client(BEARER_TOKEN)

count = client.get_recent_tweets_count(query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', granularity='day')
total_count = count[3]['total_tweet_count']
if total_count <= 5000:
    limit = total_count
else:
    limit = 5000
# tweets = client.search_recent_tweets(query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', tweet_fields=['text'], max_results=100)
tweets = tweepy.Paginator(client.search_recent_tweets, query='(#GW2 OR #GuildWars2) -commission -RT -#commssionart -#commission -#art lang:en -is:retweet -is:quote', tweet_fields=['text'], max_results=100).flatten(limit=limit)


# Get a list of all the text from tweets
tweet_text = [x.text for x in tweets]

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
cloud = wordcloud.WordCloud(max_words=100).generate(text)

plt.imshow(cloud, interpolation='bilinear')
plt.axis('off')
plt.show()
today = date.today().strftime("%d-%B-%Y")

figure_name = today + '_WordCloud.jpg'
plt.savefig(os.path.join(os.getcwd(), 'plots', figure_name))

data_name = today + '_tweets.txt'
with open(os.path.join(os.getcwd(), 'data', data_name), 'w', encoding='utf-8') as file:
    for line in tweet_text:
        file.write('%s\n-----\n' % str(line))

