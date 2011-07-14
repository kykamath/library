'''
Created on Jul 14, 2011

@author: kykamath
'''
from mr_algorithms.mrjobwrapper import MRJobWrapper

class WordCount(MRJobWrapper):
    def mapper(self, key, value):
        for word in value.split(): yield word, 1
    def reducer(self, key, values): yield key, sum(values)
    
if __name__ == '__main__':
    WordCount.run()