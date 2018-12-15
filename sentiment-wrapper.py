#! /usr/bin/env python

import os
import sys
from twython import Twython
import json
import pandas
import csv


# Read twitter public timeline to search keyword and return matched tweets
# =========================================================================

TWITTER_APP_KEY = "abc"
TWITTER_APP_KEY_SECRET = "123"
TWITTER_ACCESS_TOKEN = "456"
TWITTER_ACCESS_TOKEN_SECRET = "xyz"
client = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
search = client.search(q=sys.argv[1], lang='en', count=50, result_type='popular')
tweets = search['statuses']

os.remove("./data/rt-polaritydata/rt-reviews.raw")

for tweet in tweets: 
	with open("./data/rt-polaritydata/rt-reviews.raw","a") as fd:
        	fd.write(" ".join(tweet['text'].split()).encode('utf-8') + "\n")
		                               

# Read input and write to the raw_reviews_file
# =================================================
if len(sys.argv) > 2:
	with open("./data/rt-polaritydata/rt-reviews.raw","a") as fd:
		fd.write(sys.argv[2] + "\n")
		sys.stdout.flush()


# Deep Code Section - Runs Evaluation by CNN Model (by Denny Britz @ Google Brain - train model and run eval after installing the CNN application @ https://github.com/dennybritz/cnn-text-classification-tf (Change eval.py to read user input file generated above)
# =======================================================================================================================================================================================================================================================================
os.system("./eval.py --eval_train --checkpoint_dir='./runs/1484708861/checkpoints/'")


# Read raw reviews and append it with wordcounts
# =================================================		 

with open("./runs/1484708861/checkpoints/../prediction.csv","r+") as fin:
    with open("./data/rt-polaritydata/words.csv","w+") as fout:
        for line in fin:
			line1 = line.replace('1.0', '~ThumbsUp')
			line2 = line1.replace('0.0', '~ThumbsDown')
			line3 = ' '.join(line2.split(','))
			line4 = line3.split()
			line5 = [x for x in line4 if "http" not in x]
			line6 = ' '.join(line5)
			fout.write(line6 + "\n")

with open("./data/rt-polaritydata/words.csv","r+") as fin:
	with open("./data/rt-polaritydata/word_count.csv","w+") as fout:
		wordcount={}
		for word in fin.read().split():
			if len(word) > 4 :
				if word not in wordcount :
					wordcount[word] = 1
				else:
					wordcount[word] += 1
		for k,v in wordcount.iteritems() :
			fout.write(k + "," + str(v) + "\n")
			
		   
df = pandas.read_csv('./data/rt-polaritydata/word_count.csv', header = None, names = ['value', 'count'],delimiter=",", quoting=csv.QUOTE_NONE,  encoding='utf-8')
dlist = df.to_dict('records')
dlist = [json.dumps(record)+"\n" for record in dlist ]
with open('./data/rt-polaritydata/cloudTags.json','w') as jsonfile:
	jsonfile.writelines(dlist)
    
    
with open("./data/rt-polaritydata/words.csv","r+") as fin:
	with open("./data/rt-polaritydata/reviews.csv","w+") as fout:
		for line in fin:
			line1 = line.split('~')
			line2 = ','.join(line1)
			fout.write(line2.strip())
			fout.write('\n')

	
df = pandas.read_csv('./data/rt-polaritydata/reviews.csv', header = None, names = ['review', 'isPositive'],delimiter=",", quoting=csv.QUOTE_NONE,  encoding='utf-8')
dlist = df.to_dict('records')
dlist = [json.dumps(record)+"\n" for record in dlist]
with open('./data/rt-polaritydata/reviews.json','w') as jsonfile:
	jsonfile.writelines(dlist)
