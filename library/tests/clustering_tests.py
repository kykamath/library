'''
Created on Jun 21, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from clustering import EvaluationMetrics, EMTextClustering, KMeansClustering

class EvaluationMetricsTests(unittest.TestCase):
    def setUp(self):
        self.clusters = [['sports', 'sports', 'sports', 'sports'],
                    ['entertainment', 'entertainment', 'sports', 'entertainment'],
                    ['technology', 'technology', 'politics', 'technology'],
                    ['politics', 'politics', 'politics', 'politics']
                    ]
    def test_getpurityForClusters(self): self.assertEqual(0.875, EvaluationMetrics.getValueForClusters(self.clusters, EvaluationMetrics.purity))
    def test_getpurityForClustersWithEmpltyClusters(self): self.assertEqual(0.0, EvaluationMetrics.getValueForClusters([[]], EvaluationMetrics.purity))
    def test_getNMIForClusters(self): print EvaluationMetrics.getValueForClusters(self.clusters, EvaluationMetrics.nmi)
    
#class ClusteringTests(unittest.TestCase):
#    def test_emClustering(self):
#        documents = [
#                     (1, 'a b c d f g'),
#                     (2, 'a b c d t h'),
#                     (3, '1 2 3 4 5'),
#                     (4, '1 2 3 ')
#                     ]
#        print EMTextClustering(documents,2).cluster()
#    def test_kmeansClustering(self):
#        documents = [
#                     (1, 'a b c d f g'),
#                     (2, 'a b c d t h'),
#                     (3, '1 2 3 4 5'),
#                     (4, '1 2 3 ')
#                     ]
#        clusters = KMeansClustering(documents,2).cluster()
#        self.assertTrue(clusters[0]==clusters[1] and clusters[2]==clusters[3])
if __name__ == '__main__':
    unittest.main()