'''
Created on Jul 11, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from nlp import StopWords, getWordsFromRawEnglishMessage

class GeneralMethodsTests(unittest.TestCase):
    def test_getWordsFromRawEnglishMessage(self):
        self.assertEqual(['existing', 'distutils', 'code'], getWordsFromRawEnglishMessage('the existing distutils code'))

class StopWordsTests(unittest.TestCase):
    def test_basicFunction(self):
        self.assertTrue(StopWords.contains('the'))
        self.assertTrue(StopWords.contains('#ff'))
        self.assertFalse(StopWords.contains('africa'))
        self.assertEqual(264, len(StopWords.set))
if __name__ == '__main__':
    unittest.main()