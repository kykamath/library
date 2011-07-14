'''
Created on Jul 13, 2011

@author: kykamath
'''
import unittest
from mr_algorithms import MRWordCount

class MRWordCountTests(unittest.TestCase):
    def setUp(self):
        self.testString='Sachin Tendulkar is one century away from reaching 100 international'
        self.mrjob = MRWordCount()
    def test_mapper(self): self.assertEqual([(w,1)for w in self.testString.split()], list(self.mrjob.mapper('', self.testString)))
    def test_reducer(self): self.assertEqual([('foo', 2)], list(self.mrjob.reducer('foo', [1, 1])))

if __name__ == '__main__':
    unittest.main()
