'''
Created on Jun 21, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from clustering import EvaluationMetrics, EMTextClustering, KMeansClustering, getItemClustersFromItemsets,\
    MultistepItemsetClustering

class ItemsetClusterTests(unittest.TestCase):
    def setUp(self):
        def compare(i,j):
            d = i-j
            if d<0: return d*-1
            else: return d
        self.distanceFunction = compare
    def test_getItemClustersFromItemsetsVanilla(self):
        itemsets = [[1,2,3,4], [5,6,7,8]]
        self.assertEqual([set([1, 2, 3, 4]), set([8, 5, 6, 7])], getItemClustersFromItemsets(itemsets, self.distanceFunction))
    def test_getItemClustersFromItemsetsWithMajority(self):
        itemsets = [[1,2,3,4], [1,2,3,8]]
        self.assertEqual([set([1, 2, 3, 4, 8])], getItemClustersFromItemsets(itemsets, self.distanceFunction))
    def test_getItemClustersFromItemsetsWithoutMajority1(self):
        itemsets = [[1,2,3,4], [1,2,7,8]]
        self.assertEqual([set([1, 2, 3, 4, 7, 8])], getItemClustersFromItemsets(itemsets, self.distanceFunction))
    def test_getItemClustersFromItemsetsWithoutMajority2(self):
        itemsets = [[1,2], [7,8], [1,7,3,6]]
        self.assertEqual([set([1, 2, 3]), set([ 6, 7, 8])], getItemClustersFromItemsets(itemsets, self.distanceFunction))
        
#class MultistepClusteringTests(unittest.TestCase):
#    def setUp(self):
#        def compare(i,j):
#            d = i-j
#            if d<0: return d*-1
#            else: return d
#        self.distanceFunction = compare
#    def test_getItemClustersFromItemsetsVanilla(self):
#        itemsets = [[1,2,3,4], [5,6,7,8]]
#        self.assertEqual([[1, 2, 3, 4], [8, 5, 6, 7]], MultistepItemsetClustering().cluster(itemsets, self.distanceFunction, mergeThreshold=0.0))
#    def test_getItemClustersFromItemsetsWithMajority(self):
#        itemsets = [[1,2,3,4], [1,2,3,8]]
#        self.assertEqual([[8, 1, 2, 3, 4]], MultistepItemsetClustering().cluster(itemsets, self.distanceFunction, mergeThreshold=0.0))
#    def test_getItemClustersFromItemsetsWithoutMajority1(self):
#        itemsets = [[1,2,3,4], [1,2,7,8]]
#        self.assertEqual([[1, 2, 3, 4, 7, 8]], MultistepItemsetClustering().cluster(itemsets, self.distanceFunction, mergeThreshold=0.0))
#    def test_getItemClustersFromItemsetsWithoutMajority2(self):
#        itemsets = [[1,2], [7,8], [1,7,3,6]]
#        self.assertEqual([[1, 2, 3, 6, 7, 8]], MultistepItemsetClustering().cluster(itemsets, self.distanceFunction, mergeThreshold=0.0))
#    def test_getItemClustersFromItemsetsWithoutMajority3(self):
#        itemsets = [[1,2], [7,8], [1,7,3,6], [9,10], [7,9]]
#        self.assertEqual([[1, 2, 3, 6, 7, 8, 9, 10]], MultistepItemsetClustering().cluster(itemsets, self.distanceFunction, mergeThreshold=0.0))
#    def test_getItemClustersFromItemsetsWithoutMajority4(self):
#        itemsets = [[1,2], [7,8], [1,7,3,6], [9,10]]
#        self.assertEqual([[1, 2, 3, 6, 7, 8], [9, 10]], MultistepItemsetClustering().cluster(itemsets, self.distanceFunction, mergeThreshold=0.0))

class EvaluationMetricsTests(unittest.TestCase):
    def setUp(self):
        self.clusters = [['sports', 'sports', 'sports', 'sports'],
                    ['entertainment', 'entertainment', 'sports', 'entertainment'],
                    ['technology', 'technology', 'politics', 'technology'],
                    ['politics', 'politics', 'politics', 'politics']
                    ]
    def test_getpurityForClusters(self): self.assertEqual(0.875, EvaluationMetrics.getValueForClusters(self.clusters, EvaluationMetrics.purity))
    def test_getpurityForClustersWithEmpltyClusters(self): self.assertEqual(0.0, EvaluationMetrics.getValueForClusters([[]], EvaluationMetrics.purity))
    def test_getNMIForClusters(self): self.assertEqual('%0.3f'%0.783, '%0.3f'%EvaluationMetrics.getValueForClusters(self.clusters, EvaluationMetrics.nmi))
    def test_getNMIForPerfectClusters(self): self.assertEqual(1.0, EvaluationMetrics.getValueForClusters([[1,1], [1,1], [1,1]], EvaluationMetrics.nmi))
    def test_getF1ForClusters(self): print EvaluationMetrics.getValueForClusters(self.clusters, EvaluationMetrics.f1)
    
class ClusteringTests(unittest.TestCase):
    def setUp(self):
        self.documents = [
                     (1, 'a b c d f g'),
                     (2, 'a b c d d d t h'),
                     (3, '1 2 3 4 5'),
                     (4, '1 2 3 ')
                     ]
    def test_emClustering(self):
        print EMTextClustering(self.documents,2).cluster()
    def test_kmeansClustering(self):
        clusters = KMeansClustering(self.documents,2).cluster()
        self.assertTrue(clusters[0]==clusters[1] and clusters[2]==clusters[3])
        
if __name__ == '__main__':
    unittest.main()