'''
Created on Sep 5, 2011

@author: kykamath
'''
import unittest
import networkx as nx
from graphs import plot, CompoundNode, getMincutTree, MinCutTree
import matplotlib.pyplot as plt

class GraphTests(unittest.TestCase):
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
#    def test_plot(self):
#        colors=range(20)
#        plot(nx.star_graph(20), draw_edge_labels=True, node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)
    def test_getMincutTree(self):
        mincutTree = getMincutTree(self.graph)
        self.assertEqual([1, 2, 3, 4, 5, 6], mincutTree.nodes())
        self.assertEqual([(1, 2, {'capacity': 18}), (2, 6, {'capacity': 17}), (3, 5, {'capacity': 15}), (4, 5, {'capacity': 14}), (5, 6, {'capacity': 13})], mincutTree.edges(data=True))
    
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
        

if __name__ == '__main__':
    unittest.main()