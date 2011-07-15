'''
Created on Jul 14, 2011

@author: kykamath
'''
import sys, os
sys.path.append('../../../')
import unittest
from mr_algorithms.demo.using_options import UsingOptions

testString='Sachin Tendulkar is one century away from reaching 100 international'
log1 = '../../../data/log1'

class MRJobWrapperTests(unittest.TestCase):
    def setUp(self):
        self.usingOptions = UsingOptions(args='-r inline'.split())
    def test_mapper(self): self.assertEqual([(w+':ilab:',1)for w in testString.split()], list(self.usingOptions.mapper('', testString)))
    def test_reducer(self): self.assertEqual([('foo', 2)], list(self.usingOptions.reducer('foo', [1, 1])))
    def test_runJob(self): 
        for object in [self.usingOptions, UsingOptions('-r hadoop'.split()) if os.uname()[1]=='spock' else UsingOptions(args='-r inline'.split())]:
            self.assertEqual([(w+':ilab:',1)for w in sorted(testString.split())], list(object.runJob(inputFileList=[log1])))

if __name__ == '__main__':
    unittest.main()