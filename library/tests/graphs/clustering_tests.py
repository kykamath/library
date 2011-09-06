'''
Created on Sep 5, 2011

@author: kykamath
'''
import sys
sys.path.append('../../')
import unittest
import networkx as nx
from graphs_tests import graph, graph2
from graphs.clustering import clusterUsingMincutTrees

testGraph = graph2

class ClusteringTests(unittest.TestCase):
    def test_clusterUsingMincutTrees(self):
        print clusterUsingMincutTrees(graph, alpha=3)

if __name__ == '__main__':
    unittest.main()