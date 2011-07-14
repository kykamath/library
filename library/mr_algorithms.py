'''
Created on Jul 13, 2011

@author: kykamath
'''
from mrjob.job import MRJob

class MRJobWrapper(MRJob):
    '''
    A wrapper for MRJob. This defines some methods that I
    will be using regularly.
    '''
    def __init__(self, *args, **kwargs):
        super(MRJobWrapper, self).__init__(*args, **kwargs)
    def runJob(self, inputFileList):
        self.args = inputFileList
        with self.make_runner() as runner:
            runner.run()
            for line in runner.stream_output(): yield self.parse_output_line(line)
class WordCountSample1(MRJobWrapper):
    def mapper(self, key, value):
        for word in value.split(): yield word, 1
    def reducer(self, key, values): yield key, sum(values)
    
class WordCountSample2(MRJobWrapper):
    def get_words(self, key, line):
        for word in line.split():
            yield word, 1
    def sum_words(self, word, occurrences):
        yield word, sum(occurrences)
    def steps(self):
        return [self.mr(self.get_words, self.sum_words),]
    
class KMeans(MRJobWrapper):
    '''
    A MR implementation for kMeans.
    This is a port of MR-kmeans code written for hadoopy by Brandyn White (http://brandynwhite.com/).
    The original source code is at: https://github.com/bwhite/hadoop_vision/tree/master/kmeans 
    '''
    pass

if __name__ == '__main__':
    '''
    python mr_algorithms.py < data/log_data > output
    '''
    WordCountSample2.run()
        