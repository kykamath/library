'''
Created on Sep 5, 2011

@author: kykamath
'''
import sys
sys.path.append('../../')
import unittest
from graphs_tests import graph, graph2, graph3
from graphs.clustering import clusterUsingMincutTrees, clusterUsingMCLClustering
import networkx as nx
from graphs import plot

testGraph = graph2

class ClusteringTests(unittest.TestCase):
    def test_clusterUsingMincutTrees(self):
        self.assertEqual([[2, 1, 6, 5, 3, 4]], clusterUsingMincutTrees(graph, alpha=3.6))
        self.assertEqual([[3, 1, 2, 4], [8, 7], [6, 5]], clusterUsingMincutTrees(graph3, alpha=2))
    def test_clusterUsingMCLClustering(self):
        G=nx.random_geometric_graph(200,0.125)
        plot(G)
        clusterUsingMCLClustering(G, plot=True)

if __name__ == '__main__':
    unittest.main()