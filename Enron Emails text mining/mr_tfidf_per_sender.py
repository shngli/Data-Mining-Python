# Author: Sheng Li
# MapReduce 3: Per-Sender TF-IDFs
# The third MapReduce multiplies per-sender term frequencies by per-term IDFs. 
# This means it needs to take as input the IDFs calculated in the last step and calculate 
# the per-sender TFs. That requires something we haven't seen yet: initialization logic. 

import os
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

DIRECTORY = "/Users/[username]/Desktop/idf_parts/"

class MRTFIDFBySender(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        for term in get_terms(email['text']):
            yield {'term': term, 'sender': email['sender']}, 1

    def reducer_init(self):
        self.idfs = {}
        for fname in os.listdir(DIRECTORY): # look through file names in the directory
            file = open(os.path.join(DIRECTORY, fname)) # open a file
            for line in file: # read each line in json file
                term_idf = JSONValueProtocol().read(line)[1] # parse the line as a JSON object
                self.idfs[term_idf['term']] = term_idf['idf']

    def reducer(self, term_sender, howmany):
        tfidf = sum(howmany) * self.idfs[term_sender['term']]
        yield None, {'term_sender': term_sender, 'tfidf': tfidf}

if __name__ == '__main__':
    MRTFIDFBySender.run()
    
# python mr_tfidf_per_sender.py -o 'sender_tfidf' --no-output 'lay-k.json'