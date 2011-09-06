'''
Created on Sep 5, 2011

@author: kykamath
'''
from graphs import plot, getMincutTree
from networkx.algorithms.components.connected import connected_components

def clusterUsingMincutTrees(graph, alpha):
    ''' Mincut clustering as described in 
        "Graph Clustering and Minimum Cut Trees" - Gary William Flake, Robert E. Tarjan & Kostas Tsioutsiouliklis (http://www.tandfonline.com/doi/abs/10.1080/15427951.2004.10129093#preview)
    '''
    t_node = ':ilab:t:ilab:'
    for n in graph.nodes_iter(): graph.add_edge(n, t_node, capacity=alpha)
#    plot(graph, draw_edge_labels=True)
    mincutTree = getMincutTree(graph)
#    plot(mincutTree, draw_edge_labels=True)
    mincutTree.remove_node(t_node)
    return connected_components(mincutTree)

if __name__ == '__main__':
    a = [[1,2],[3,4,5]]
    from itertools import product
    print list(product(*a))
        