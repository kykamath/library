'''
Created on Oct 4, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from frequent_itemsets import Eclat

class EclatTests(unittest.TestCase):
    def test_testGetFrequentItemsets(self): 
        minsup = 3
        data1 = [['a','b','c'],['b','c'],['b','c'], ['a','d','e'], ['b','c','d'], ['b','c','e']]
        data2 = [[1,2,3],[2,3],[2,3], [1,4,5], [2,3,4], [2,3,5]]
        self.assertEqual([(['b'], 5), (['b', 'c'], 5), (['c'], 5)], Eclat(data1, minsup).getFrequentItemsets())
        self.assertEqual([([2], 5), ([2, 3], 5), ([3], 5)], Eclat(data2, minsup).getFrequentItemsets())
    
if __name__ == '__main__':
    unittest.main()