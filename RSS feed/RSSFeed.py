# Author: Chisheng Li
# Program: Retrieving RSS feed


import feedparser
import re
import string

# Create the regular expressions
reg1 = re.compile(r'<br />') #Regex to replace <br /> with \n (see reg1.sub)
reg2 = re.compile(r'(<!--.*?-->|<[^>]*>)') #Regex to clean all html tags (anything with <something>)

# Alternative reg2
#reg2 = re.compile(r'<[^<]+?>')
#reg2 = re.compile(r'<[^>]+>')

reg3 = re.compile(r'&nbsp') #Regex to clean all &nbsp 
reg4 = re.compile(r'\'') #Regex to clean all ' chars
# Alternative reg4
#reg4 = re.compile(r"'")

# Parses the RSS feed from RSS
def parseFeeds( str ):
    d = feedparser.parse(str)
    print "There are", len(d['items']), "items in", str
    FILE_INPUT = open("NewsFeed.txt","w")
    for item in d['items']:
    	first_filter = reg1.sub('\n', item.description)
    	second_filter = reg2.sub('', first_filter)
    	third_filter = reg3.sub(' ', second_filter)
    	item_description = reg4.sub('', third_filter)
    try:
    	FILE_INPUT.write(item_description)
    except IOError:
    	print "Error: can\'t find file or read data"
    FILE_INPUT.close

#Main     
if __name__ == '__main__':
    # Provide a link to an RSS Feed
    parseFeeds("http://rss.cnn.com/rss/cnn_topstories.rss")

# Alternative links to parse 
# parseFeeds("http://sports.espn.go.com/espn/rss/news") 
# parseFeeds("http://www.reddit.com/r/python/.rss")