'''
Created on Jul 14, 2011

@author: kykamath
'''
from mrjobwrapper import ModifiedMRJob
class WordCountMRJob(ModifiedMRJob):
    def mapper(self, key, value):
        for word in value.split(): yield word, 1
    def reducer(self, key, values): yield key, sum(values)
    
if __name__ == '__main__':
    WordCountMRJob.run()