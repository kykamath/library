'''
Created on Sep 5, 2011

@author: kykamath
'''
from graphs import plot, getMincutTree, CUT_CLUSTERING_T_NODE,\
    getMincutTreeForCutClustering
from networkx.algorithms.components.connected import connected_components
import networkx as nx
from graphs import plot as graphPlot
import matplotlib.pyplot as plt
import os

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

def clusterUsingMCLClustering(graph, plot=False, graphClass=nx.Graph, inflation=1.4, **kwargs):
    ''' Uses Markov Cluster Algorithm described in http://micans.org/mcl/.
    '''
    def getClusters(data, inflation=1.4):
        clusters = []
        if data:
            os.environ["PATH"] = os.environ["PATH"]+os.pathsep+'/opt/local/bin'
            mcl_folder = '/tmp/mcl_dir/'
            if not os.path.exists(mcl_folder): os.mkdir(mcl_folder)
            os.chdir(mcl_folder)
            graph_file = open('graph', 'w')
            for edge in data: graph_file.write('%s %s %d\n'%(edge))
            graph_file.close()
            os.system('mcl graph -q x -V all -I %s --abc -o graph.out'%inflation)
            for l in open('graph.out'): clusters.append(l.strip().split())
            os.system('rm -rf /tmp/mcl_dir/*')
        return clusters
    edges, nodeToCluster = [], {}
    for e in graph.edges_iter(data=True):
        if 'w' in e[2]: edges.append((e[0], e[1], e[2]['w']))
        else: edges.append((e[0], e[1], 1))
    clusterId = 0
    for cluster in getClusters(edges, inflation=inflation):
        for n in cluster: nodeToCluster[n]=clusterId
        clusterId+=1
    clusterdGraph = graphClass()
    for n, data in graph.nodes_iter(data=True): clusterdGraph.add_node(n, data)
    for u, v, data in graph.edges_iter(data=True):
        if nodeToCluster[str(u)]==nodeToCluster[str(v)]: clusterdGraph.add_edge(u, v, data)
    if plot: graphPlot(clusterdGraph, **kwargs)
    return clusterdGraph

if __name__ == '__main__':
    a = [[1,2],[3,4,5]]
    from itertools import product
    print list(product(*a))
        