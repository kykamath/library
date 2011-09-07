'''
Created on Sep 5, 2011

@author: kykamath
'''
import sys
from tests.graphs.graphs_tests import graph3
sys.path.append('../../')
import unittest
from graphs_tests import graph, graph2
from graphs.clustering import clusterUsingMincutTrees

testGraph = graph2

class ClusteringTests(unittest.TestCase):
    def test_clusterUsingMincutTrees(self):
        self.assertEqual([[1, 2, 3, 4, 5, 6]], clusterUsingMincutTrees(graph, alpha=3.6))
        self.assertEqual([[1, 2, 3, 4], [5, 6], [8, 7]], clusterUsingMincutTrees(graph3, alpha=2))

if __name__ == '__main__':
    unittest.main()