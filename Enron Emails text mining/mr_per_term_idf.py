# Author: Sheng Li
# MapReduce 2: Per-Term IDF
# What we want to do here is emit log(516893.0 / # documents with wordX) for each wordX 
# in our dataset. Notice the decimal on 516893.0: that's so we do floating point division 
# rather than integer division. The output should be a file where each line contains 
# {'term': 'wordX', 'idf': 35.92} for actual values of wordX and 35.92.

import math
import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRTermIDF(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        terms = set(get_terms(email['text']))
        for term in terms:
            yield term, 1

    def reducer(self, term, howmany):
        idf = math.log(516893.0 / sum(howmany))
        yield None, {'term': term, 'idf': idf}

if __name__ == '__main__':
        MRTermIDF.run()

# python mr_per_term_idf.py -o 'idf_parts' --no-output 'lay-k.json'