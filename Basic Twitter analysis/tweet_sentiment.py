# Author: Chisheng Li
# Derive the tweet sentiment with $python tweet_sentiment.py AFINN-111.txt output.txt
# Any word not in AFINN-111.txt should be given a score of 0.
import sys
import json
import re

#Read the sentiment file and create a dictionary with the values
def build_dict(fn):
	#open AFINN-111.txt
	afinnfile = open(fn)
	#initialize an empty dictionary
	scores = {}
	for line in afinnfile:
		# The file is tab-delimited. "\t" means "tab character"
		term, score = line.split("\t")
		# Convert the score to an integer.
		scores[term] = int(score)
	return scores

#Read the tweet file and build a dctionary containing tweet text.
def extract_tweets(fn):
	#open output.txt
	tweets_file = open(fn)
	#initialze an empty array
	tweets = []
	for tweet in tweets_file:
		#Parse input strings as Json
		json_tweet = json.loads(tweet)
		#Check that there is a text field.
		if "text" in json_tweet.keys():
			text = json_tweet["text"].encode('utf-8')
			tweets.append(text)	
	return tweets

#Compile a sentiment score for every tweet in a list.
def judge_sentiments(tweets, sentiments):
	for tweet in tweets:
		tweet_score = 0
		tweet_words = re.findall(r"[\w']+", tweet)
		
		for word in tweet_words:
			word_score = sentiments[word.lower()] if word.lower() in sentiments else 0
			#Keep adding the sentiment for the entire single tweet. 
			tweet_score += word_score
		#Output the sentiment score for each tweet as a float
		print float(tweet_score)
		
def main():
	scores = build_dict(sys.argv[1])
	tweets = extract_tweets(sys.argv[2])
	sentiments = judge_sentiments(tweets, scores)

if __name__ == '__main__':
    main()