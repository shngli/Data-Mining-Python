The updated Yelp academic dataset is available [here](http://www.yelp.com/dataset_challenge/). This Yelp analysis uses the file yelp_academic_dataset_review.json downloaded on Jan 14th 2015.

1. review_word_count.py sorts the number of terms (including symbols and numbers) that appear in all the review texts. **Output**: reviewWordCount.txt
2. unique_review.py finds the review_id that has the most number of unique terms in its review text. **Output**: unique.txt
3. user_similarity.py outputs the pair of user IDs where their Jaccard similarity is greater than or equal to 0.5, based on the set of IDs of the businesses reviewed by each user. Note the output is too large to be uploaded.
