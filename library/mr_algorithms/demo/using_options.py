'''
Created on Jul 15, 2011

@author: kykamath
'''
import sys
sys.path.append('../../')
from mrjobwrapper import MRJobWrapper
from mr_algorithms.demo.using_options_mr import UsingOptionsMRJob

class UsingOptions(MRJobWrapper):
    def __init__(self, args='-r hadoop'.split()):
        self.mrjob = UsingOptionsMRJob(args=args)