'''
Created on Jul 14, 2011

@author: kykamath
'''
import sys
sys.path.append('../../../')
from mr_algorithms.demo.word_count import WordCount
import unittest, os

testString='Sachin Tendulkar is one century away from reaching 100 international'
log1 = '../../../data/log1'

class WordCountTests(unittest.TestCase):
    def setUp(self):
        self.wordCount = WordCount(args='-r inline'.split())
    def test_mapper(self): self.assertEqual([(w,1)for w in testString.split()], list(self.wordCount.mapper('', testString)))
    def test_reducer(self): self.assertEqual([('foo', 2)], list(self.wordCount.reducer('foo', [1, 1])))
    def test_runJob(self): 
        self.assertEqual([(w,1)for w in sorted(testString.split())], list(self.wordCount.runJob(inputFileList=[log1])))
    def test_forHadoopOnly(self):
        if os.uname()[1]=='spock':
            wcSample1 = WordCount(args='-r hadoop'.split())
            self.assertEqual([(w,1)for w in sorted(testString.split())], list(wcSample1.runJob(inputFileList=[log1])))
        else: print 'Not running hadoop specific tests.'
    def test_runMapper(self): self.assertEqual([(w,1)for w in testString.split()], list(self.wordCount.runMapper(inputFileList=[log1])))


if __name__ == '__main__':
    unittest.main()