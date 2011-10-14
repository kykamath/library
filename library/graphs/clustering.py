'''
Created on Sep 5, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
from graphs import CUT_CLUSTERING_T_NODE, getMincutTreeForCutClustering
    
def clusterUsingMincutTrees(graph, alpha):
    ''' Mincut clustering as described in 
        "Graph Clustering and Minimum Cut Trees" - Gary William Flake, Robert E. Tarjan & Kostas Tsioutsiouliklis (http://www.tandfonline.com/doi/abs/10.1080/15427951.2004.10129093#preview)
    '''
    for n in graph.nodes_iter(): graph.add_edge(n, CUT_CLUSTERING_T_NODE, capacity=alpha)
    mincutTree = getMincutTreeForCutClustering(graph)
    components = []
    for n in mincutTree.nodes()[:]:
        if CUT_CLUSTERING_T_NODE not in n.vertices: components.append(n.vertices)
    return components

if __name__ == '__main__':
    a = [[1,2],[3,4,5]]
    from itertools import product
    print list(product(*a))
        