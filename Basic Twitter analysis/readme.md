The scripts query and analyse Twitter's live stream data as follow:

Need `easy_install ouath2` to access Twitter stream.

1. **print.py:** prints out the text of live tweets. Save the tweets with `$ python print.py > output.txt`.
2. **twitterstream.py:** accesses live Twitter stream and pipe the output into output.txt. Let the script runs for 10 mins and terminate it with Crtl+c. Output the live tweets as `$ python twitterstream.py > output.txt` or `$ python twitterstream.py > output.json`.
3. **tweet_sentiment.py:** derive the sentiment of each tweet by assigning a score using AFINN-111.txt. Run the script as `$ python tweet_sentiment.py AFINN-111.txt output.txt`.
4. **frequency.py:** computes the term frequency histogram of the livestream data in output.txt. Run the script as `$ python frequency.py output.txt`.
5. **top_ten.py:** counts the top 10 most frequent hash tags from output.txt. Run the script as `$ python top_ten.py output.txt`.
