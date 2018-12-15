#! /usr/bin/env python

import os
import tweepy
import pandas as pd

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

trends1 = api.trends_place(23424848)
data = trends1[0]
trends = data['trends']
names1 = [trend['name'] for trend in trends]
names = names1[:5]
trendsName = ' '.join(names)
print(trendsName)

for name in names:
    #os.remove('./data/%s' % name)
    for tweet in tweepy.Cursor(api.search,
                               q=name,
                               rpp=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items(1000):
        with open('./data/%s' % name,"a") as fd:
            fd.write(str(tweet.user.friends_count).encode('utf-8')+","+
                    tweet.user.screen_name.encode('utf-8')+","+
                    str(tweet.user.followers_count).encode('utf-8')+"\n")
            
    df=pd.read_csv('./data/%s' % name, header=None, names=list('ABC'))
    a=len(df[df.A>500].index)
    b=len(df.index)
    print str(name), " trend is currently" ,str("%.2f" % ((float(1) - float(a)/float(b)) * float(100))), "% organic"
