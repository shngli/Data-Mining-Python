# Author: Sheng Li
# Create a second version of the MapReduce wordcounter that counts the number of each word 
# emitted by each sender. You will need this for later, since we're going to be calculating 
# TF-IDF implementing terms per sender. 

import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRWCBySender(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        for term in get_terms(email['text']):
            yield {'term': term, 'sender': email['sender']}, 1

    def reducer(self, term_sender, occurrances):
        yield None, {'term_sender': term_sender, 'count': sum(occurrances)}

if __name__ == '__main__':
        MRWCBySender.run()

# python mr_wc_by_sender.py -o 'wc_by_sender' --no-output 'lay-k.json'