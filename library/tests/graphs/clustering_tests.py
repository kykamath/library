'''
Created on Sep 5, 2011

@author: kykamath
'''
import unittest
import networkx as nx
from graphs.clustering import MinCutClustering

class MinCutClusteringTests(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.graph.add_edge(1, 2, capacity=10)
        self.graph.add_edge(2, 3, capacity=4)
        self.graph.add_edge(3, 4, capacity=5)
        self.graph.add_edge(4, 5, capacity=7)
        self.graph.add_edge(5, 6, capacity=3)
        self.graph.add_edge(6, 1, capacity=8)
        self.graph.add_edge(2, 6, capacity=3)
        self.graph.add_edge(3, 5, capacity=4)
        self.graph.add_edge(2, 5, capacity=2)
        self.graph.add_edge(3, 6, capacity=2)
        self.graph.add_edge(6, 4, capacity=2)
    def test_cluster(self):
        MinCutClustering.cluster(self.graph)

if __name__ == '__main__':
    unittest.main()