'''
Created on Jul 14, 2011

@author: kykamath
'''
import sys
from mr_algorithms.demo.word_count_mr import WordCountMRJob
from mrjobwrapper import CJSONProtocol
sys.path.append('../../../')
import unittest

test_document='Sachin Tendulkar is one century away from reaching 100 international'
log1 = '../../../data/log1'
with open(log1, 'w') as f: f.write(CJSONProtocol.write('doc_id_1', test_document)+'\n')

class WordCountTests(unittest.TestCase):
    def setUp(self): self.wordCount = WordCountMRJob(args='-r inline'.split())
    def test_mapper(self): self.assertEqual([(w,1)for w in test_document.split()], list(self.wordCount.mapper('doc_id_1', test_document)))
    def test_reducer(self): self.assertEqual([('foo', 2)], list(self.wordCount.reducer('foo', [1, 1])))
    def test_runJob(self): 
        jobRunOutput = list(self.wordCount.runJob(inputFileList=[log1], jobconf={'mapred.reduce.tasks':2}))
        self.assertEqual([(w,1)for w in sorted(test_document.split())], jobRunOutput)

if __name__ == '__main__':
    unittest.main()