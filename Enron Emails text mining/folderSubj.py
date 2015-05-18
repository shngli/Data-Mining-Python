# Author: Sheng Li
# Compare the most similar folders by the email subject line (e['subject'])

import os, sys, math
from email_util import *
from collections import Counter, defaultdict

import nltk
stemmer = nltk.stem.porter.PorterStemmer()

import re
refs_pat = '^[a-z][a-z\'-]+[a-z]$'
refs_prog = re.compile(refs_pat)
NAMEWORDS = set()

# l2norm() function to divide a person's TF value by the l2norm of the term vector 
def l2norm(vec):
    return float(math.sqrt(sum(map(lambda (term, c): c**2, vec))))

# get_terms() to perform all of the data cleaning
def get_terms(s):
	# Casing and short words
	# We can deal with these by lower-casing all of the terms and filtering out the short terms.
	# We also want to remove lines that begins with '>' which is typical in emails that were 
	# forwarded or replied to
	s = s.lower()
	lines = filter(lambda line: not line.strip().startswith(">"), s.split('\n'))
	arr = '\n'.join(lines).split()
	terms = []
	for term in arr:
		if re.match(refs_pat, term) != None:
			terms.append(term)
	terms = map(lambda term: term.replace("'s",'').replace("'", '').replace(".", "").replace(",", ""), terms)
	terms = filter(lambda term: len(term) > 3, terms)
	# Stop Words
	# The email_util module defines a variable STOPWORDS that contains a list of common english 
	# stop words in lower case. We can filter out terms that are found in in this list.
	from email_util import STOPWORDS
	terms = filter(lambda term: term not in STOPWORDS, terms)
	# Remove names from the terms
	terms = filter(lambda term: term not in NAMEWORDS, terms)
	terms = filter(stemmer.stem, terms)
	return terms

for e in EmailWalker('lay-k'):
	NAMEWORDS.update(e['names'])

# To calculate term frequency
folder_tf = defaultdict(Counter)

for e in EmailWalker('lay-k'):
    terms_in_email = get_terms(e['subject'])
    folder_tf[e['folder']].update(terms_in_email)

# To calculate inverse document frequency
terms_per_folder = defaultdict(set)
nemails = 0
for e in EmailWalker('lay-k'):
	terms_in_email = get_terms(e['subject'])
	# this collects all of the terms in each folder
	terms_per_folder[e['folder']].update(terms_in_email)

# Each iteration retrieves the terms for a given folder, and adds them all to the counter.
allterms = Counter()
for folder, terms in terms_per_folder.iteritems():
	# this will increment the counter value for each term in `terms`
	allterms.update(terms)

# To normalize weights
for key in folder_tf.keys():
    tfs = folder_tf[key]
    normfactor = float(l2norm(tfs.iteritems()))
    for term in tfs.keys():
        tfs[term] /= normfactor

idfs = {}
# The number of keys should be the number of folders 
nfolders = len(terms_per_folder)   
for term, count in allterms.iteritems():
	idfs[term] = math.log( nfolders / (1.0 + count) )

# Calculate tf-idf for each folder
# key is folder name, value is a list of (term, tfidf score) pairs
tfidfs = {}
for folder, tfs in folder_tf.items():
	tfidfs[folder] = map(lambda (k, v): (k, v*idfs[k]), tfs.items())
	pass

# Print the top terms
f = open(r"folderSubj_TFIDF.txt", "w")
for folder, terms in tfidfs.items():
	#print folder
	f.write(folder + '\n')
	sorted_by_count_top20 = sorted(terms, key=lambda (k, v):v, reverse=True)[:20]
	for pair in sorted_by_count_top20:
		#print '\t', pair
		f.write('\t' + str(pair) + '\n')
f.close()

from math import *

# To calculate folder cosine similarity
def cal_similarity(folder1_tfidfs, folder2_tfidfs):
	# compute the similarity between the two arguments
	folder1_score = dict(folder1_tfidfs)
	folder2_score = dict(folder2_tfidfs)
	
	numerator = 0.0
	for key, valus in folder1_score.items():
		dotscore = folder1_score[key]*folder2_score.get(key, 0.0)
		numerator += dotscore
	# compute the l2 norm of each vector
	folder1_norm = math.sqrt(sum([score**2 for score in folder1_score.values()]))
	folder2_norm = math.sqrt(sum([score**2 for score in folder2_score.values()]))
	denominator = folder1_norm * folder2_norm + 1.0
	
	similarity = numerator/denominator
	return (similarity)    

def sort_by_count(key_value, top_n):
	sorted_by_count_topn = sorted(key_value, key=lambda (k, v):v, reverse=True)[:top_n]
	return (sorted_by_count_topn)

num_of_folders = len(tfidfs.keys())
folder_similarity = dict()

for i in range(0, num_of_folders-1):
	for j in range(i+1, num_of_folders):
		folder1 = tfidfs.keys()[i]
		folder2 = tfidfs.keys()[j]
		similarity = cal_similarity(sort_by_count(tfidfs[folder1], 100), sort_by_count(tfidfs[folder2], 100))
		key = '%s and %s' % (folder1, folder2)
		folder_similarity[key] = similarity        
		#print('The similarity between folder [%s] and [%s] is %.2f' % (folder1, folder2, similarity))
sorted_similarity = sort_by_count(folder_similarity.items(), len(folder_similarity))
f = open(r"folderSubj_Cosine.txt", "w")
f.write('The sorted folder similarities are:' + '\n')
#print('The sorted folder similarities are:')
for k,v in sorted_similarity:
	#print('%s: %s' % (k, v))
	f.write('%s: %s' % (k, v) + '\n')
f.close()