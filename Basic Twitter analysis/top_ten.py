#Author: Chisheng Li
#Count the top 10 hash tag with $ python top_ten.py output.txt
import sys
import json
import operator
from operator import itemgetter

#Build a dictionary containing tweet text
def dict_tweets(fn):
	tweets_file = open(fn)
	tweets = []
	for tweet in tweets_file:
		#Parse input strings as Json
		json_tweet = json.loads(tweet)
		tweets.append(json_tweet)
	
	return tweets

#Extract hash tags
def extract_htags(tweets):
	htags = []
	for tweet in tweets:
		#Ensure that there is an entities element to extract.
		if "entities" in tweet.keys() and "hashtags" in tweet["entities"]:
			for htag in tweet["entities"]["hashtags"]:
				unicode_tag = htag["text"].encode('utf-8')
				htags.append(unicode_tag)
	return htags

#Count top 10 hash tags
def top_ten(htags):
	freq = []
	for htag in htags:
		tup = [htag,htags.count(htag)]
		if tup not in freq : freq.append(tup)
	freq_sorted = sorted(freq, key=itemgetter(1), reverse=True)
	
	for i in range(0,10):
		print freq_sorted[i][0] + " " + str(float(freq_sorted[i][1]))

def main():
	#populate the list of tweets
	tweets = dict_tweets(sys.argv[1])
	#extract the hash tags
	htags = extract_htags(tweets)
	top_ten(htags)

if __name__ == '__main__':
	main()