'''
Created on Sep 5, 2011

@author: kykamath
'''
import sys
from networkx.algorithms.traversal.depth_first_search import dfs_tree
sys.path.append('../../')
import unittest
import networkx as nx
from graphs import plot, CompoundNode, getMincutTree, MinCutTree,\
    CompoundNodeForTreeCutClustering, CUT_CLUSTERING_T_NODE,\
    totalIncidentEdgeWeights, clusterUsingMCLClustering
import matplotlib.pyplot as plt

graph = nx.Graph()
graph.add_edge(1, 2, capacity=10)
graph.add_edge(2, 3, capacity=4)
graph.add_edge(3, 4, capacity=5)
graph.add_edge(4, 5, capacity=7)
graph.add_edge(5, 6, capacity=3)
graph.add_edge(6, 1, capacity=8)
graph.add_edge(2, 6, capacity=3)
graph.add_edge(3, 5, capacity=4)
graph.add_edge(2, 5, capacity=2)
graph.add_edge(3, 6, capacity=2)
graph.add_edge(6, 4, capacity=2)

graph2 = nx.Graph()
graph2.add_edge(1, 2, capacity=10)
graph2.add_edge(2, 3, capacity=13)
graph2.add_edge(3, 1, capacity=12)

graph3 = nx.Graph()
graph3.add_edge(1, 2, capacity=10)
graph3.add_edge(1, 3, capacity=10)
graph3.add_edge(2, 4, capacity=10)
graph3.add_edge(3, 4, capacity=10)
graph3.add_edge(3, 5, capacity=1)
graph3.add_edge(3, 6, capacity=1)
graph3.add_edge(5, 6, capacity=10)
graph3.add_edge(7, 6, capacity=1)
graph3.add_edge(8, 6, capacity=1)
graph3.add_edge(7, 8, capacity=10)


class GraphTests(unittest.TestCase):
    def test_plot(self):
        colors=range(20)
        plot(nx.star_graph(20), draw_edge_labels=True, node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)
    def test_getMincutTree(self):
        mincutTree = getMincutTree(graph)
        self.assertEqual([1, 2, 3, 4, 5, 6], mincutTree.nodes())
        self.assertEqual([(1, 2, {'capacity': 18}), (2, 6, {'capacity': 17}), (3, 5, {'capacity': 15}), (4, 5, {'capacity': 14}), (5, 6, {'capacity': 13})], mincutTree.edges(data=True))
        mincutTree = getMincutTree(graph2)
        self.assertEqual([1, 2, 3], mincutTree.nodes())
        self.assertEqual([(1, 3, {'capacity': 22}), (2, 3, {'capacity': 23})], mincutTree.edges(data=True))
    def test_totalIncidentEdgeWeights(self):
        self.assertEqual(22, totalIncidentEdgeWeights(graph2,1))
        self.assertEqual(18, totalIncidentEdgeWeights(graph,1))
    def test_clusterUsingMCLClustering(self):
        G=nx.random_geometric_graph(200,0.125)
        plot(G)
        clusterUsingMCLClustering(G, plotClusters=True)
    
class MinCutTreeTests(unittest.TestCase):
    def setUp(self):
        self.S1 = CompoundNode.getInstance('S1', [1, 2])
        self.S2 = CompoundNode.getInstance('S2', [3, 4, 5, 6])
        self.mincutTree = MinCutTree()
        self.mincutTree.add_edge(self.S1, self.S2, capacity=17)
    def test_getNextNonSingletonNode(self):
        n = self.mincutTree.getNextNonSingletonNode()
        self.assertEqual('S2', n)
        self.mincutTree.remove_node(n)
        n = self.mincutTree.getNextNonSingletonNode()
        self.assertEqual('S1', n)
        self.mincutTree.remove_node(n)
        self.assertEqual(None, self.mincutTree.getNextNonSingletonNode())
    def test_splitNode(self):
        S11 = CompoundNode.getInstance('S11', [1])
        S12 = CompoundNode.getInstance('S12', [2])
        self.mincutTree.splitNode(self.S1, (S11, S12, 18), [(S12, self.S2, 17)])
        self.assertEqual(set([self.S2, S11, S12]), set(self.mincutTree.nodes()))
        self.assertEqual(set([(self.S2, S12), (S11, S12)]), set(self.mincutTree.edges()))
        
class CompoundVertexTests(unittest.TestCase):
    def setUp(self):
        self.S1 = CompoundNode.getInstance('S1', [1, 2])
        self.S2 = CompoundNode.getInstance('S2', [3, 4, 5, 6])
    def test_init(self):
        graph = nx.Graph()
        graph.add_edge(self.S1, self.S2, {'capacity':17})
        self.assertEqual([('S2', 'S1', {'capacity': 17})], graph.edges(data=True))
        self.assertEqual([1,2], self.S1.vertices), self.assertEqual([3, 4, 5, 6], self.S2.vertices)
    def test_getRandomPairOfVertices(self): self.assertEqual(set([1, 2]), set(self.S1.getRandomPairOfVertices()))
    
class CompoundNodeForTreeCutClusteringTests(unittest.TestCase):
    def setUp(self):
        self.S1 = CompoundNodeForTreeCutClustering.getInstance('S1', [1, 2])
        self.S2 = CompoundNodeForTreeCutClustering.getInstance('S2', [3, 4, 5, 6])
        self.S3 = CompoundNodeForTreeCutClustering.getInstance('S3', [CUT_CLUSTERING_T_NODE, 4, 5, 6])
    def test_getNextSourceAndSink(self): 
        self.assertEqual((1, CUT_CLUSTERING_T_NODE), self.S1.getNextSourceAndSink())
        self.assertEqual((3, CUT_CLUSTERING_T_NODE), self.S2.getNextSourceAndSink())
        self.assertEqual((4, CUT_CLUSTERING_T_NODE), self.S3.getNextSourceAndSink())

if __name__ == '__main__':
    unittest.main()