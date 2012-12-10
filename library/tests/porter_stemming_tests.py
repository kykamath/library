'''
Created on Dec 10, 2012

@author: krishnakamath
'''

from porter_stemming import PorterStemmer
import unittest

class PorterStemmerTests(unittest.TestCase):
    def test_word_stemming(self):
        stemmer = PorterStemmer()
        self.assertEqual('stem', stemmer.stem_word('stem'))
        self.assertEqual('stem', stemmer.stem_word('stemmed'))
        self.assertEqual('stem', stemmer.stem_word('stemming'))
        
if __name__ == '__main__':
    unittest.main()
