'''
Created on Sep 5, 2011

@author: kykamath
'''
from graphs import plot
import networkx as nx

class MinCutClustering:
    ''' Mincut clustering as described in 
        "Graph Clustering and Minimum Cut Trees" - Gary William Flake, Robert E. Tarjan & Kostas Tsioutsiouliklis (http://www.tandfonline.com/doi/abs/10.1080/15427951.2004.10129093#preview)
    '''
    @staticmethod
    def cluster(graph, alpha):
        minCutTree = nx.Graph()
        plot(graph, draw_edge_labels=True)
        print (graph.edges(data=True))
        