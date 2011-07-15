'''
Created on Jul 14, 2011

@author: kykamath
'''
import sys
sys.path.append('../../../')
import unittest, os
from mr_algorithms.demo.using_options import WordCountUsingOptions
from StringIO import StringIO

testString='Sachin Tendulkar is one century away from reaching 100 international'
log1 = '../../../data/log1'

class MRJobWrapperTests(unittest.TestCase):
    def setUp(self):
        self.wordCount = WordCountUsingOptions(args='-r inline'.split())
    def test_mapper(self): self.assertEqual([(w+self.wordCount.options.val1,1)for w in testString.split()], list(self.wordCount.mapper('', testString)))
    def test_reducer(self): self.assertEqual([('foo', 2)], list(self.wordCount.reducer('foo', [1, 1])))
    def test_runJob(self): 
        for object in [self.wordCount, WordCountUsingOptions()]:
            self.assertEqual([(w+self.wordCount.val1,1)for w in sorted(testString.split())], list(object.runJob(inputFileList=[log1])))

if __name__ == '__main__':
    unittest.main()