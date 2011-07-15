'''
Created on Jul 15, 2011

@author: kykamath
'''
import sys
sys.path.append('../../')
from mr_algorithms.demo.word_count_mr import WordCountMRJob
from mrjobwrapper import MRJobWrapper

class WordCount(MRJobWrapper):
    def __init__(self, args):
        self.mrjob = WordCountMRJob(args=args)