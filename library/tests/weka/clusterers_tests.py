'''
Created on Nov 9, 2011

@author: kykamath
'''
import sys
sys.path.append('../../')
import unittest
from weka import Clustering

class ClusterTests(unittest.TestCase):
    def test_clusterTests(self):
        dataDict = {1: {'a':10, 'b': 15},
        2: {'c':10},
        3: {'a':10, 'b': 15}}
        self.assertEqual({1: 0, 2: 1, 3: 0}, Clustering.cluster(Clustering.KMeans, dataDict, '-N 2'))

if __name__ == '__main__':
    unittest.main()