from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

WORD_RE = re.compile(r"[\w']+")


class ReviewWordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def extract_words(self, _, record):
        """Extract words using a regular expression.  Normalize the text to
        ignore capitalization."""
        if record['type'] == 'review':
            for word in WORD_RE.findall(record['text']):
                yield [word.lower(), 1]

    def count_words(self, word, counts):
        """Summarize all the counts by taking the sum."""
        yield [word, sum(counts)]

    def steps(self):
        """Counts the number of words in all reviews
        extract_words: <line, record> => <word, count>
        count_words: <word, counts> => <word, total>
        """
        return [
            self.mr(self.extract_words, self.count_words),
        ]


if __name__ == '__main__':
    ReviewWordCount.run()
