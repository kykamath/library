'''
Created on Nov 9, 2011

@author: kykamath
'''
import sys
sys.path.append('../../')
import unittest
from weka import Clustering, ARFF

class ClusterTests(unittest.TestCase):
    def setUp(self):
        self.dataDict = {1: {'a':10, 'b': 15},
        2: {'c':10},
        3: {'a':10, 'b': 15}}
        self.fileName = ARFF.writeARFFForClustering(self.dataDict, 'test')
    def test_clusterTests(self):
        self.assertEqual({1: 0, 2: 1, 3: 0}, Clustering.cluster(Clustering.KMeans, self.fileName, self.dataDict, '-N 2'))

if __name__ == '__main__':
    unittest.main()