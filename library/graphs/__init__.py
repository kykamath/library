import sys
sys.path.append('../')
import os
import networkx as nx
import matplotlib.pyplot as plt
from random import sample
from maxflow import ford_fulkerson
from operator import itemgetter
from library.file_io import FileIO

MINCUT_TREE_NODE = 'mincut_tree_node'
CAPACITY = 'capacity'
CUT_CLUSTERING_T_NODE = ':ilab:t:ilab:'

def plot(graph, **kwargs):
    pos=kwargs.get('pos', nx.spring_layout(graph))
    if kwargs.get('draw_edge_labels', False): edge_labels=nx.draw_networkx_edge_labels(graph,pos)
    else: edge_labels=[]
    nx.draw(graph, pos, edge_labels=edge_labels, **kwargs)
#    plt.savefig('plot.pdf')
    plt.show()
    
def totalIncidentEdgeWeights(graph, node): return sum(graph[node][n]['capacity'] for n in graph.neighbors_iter(node))

class Networkx:
    @staticmethod
    def getDictForGraph(graph):
        return dict(nodes=graph.nodes(True), edges=graph.edges(data=True))
    @staticmethod
    def getGraphFromDict(data, graphClass=nx.Graph): 
        graph = graphClass()
        for node, nodeData in data['nodes']: graph.add_node(node, nodeData)
        for u, v , edgeData in data['edges']: graph.add_edge(u, v, edgeData)
        return graph
    @staticmethod
    def writeGraphToFile(graph, fileName): FileIO.writeToFileAsJson(Networkx.getDictForGraph(graph), fileName)
    @staticmethod
    def readGraphFromFile(fileName): return Networkx.getGraphFromDict(list(FileIO.iterateJsonFromFile(fileName))[0])

def clusterUsingAffinityPropagation(graph,**kwargs):
    from sklearn.cluster.affinity_propagation_ import AffinityPropagation
    S = nx.to_numpy_matrix(graph, weight='w')
    af = AffinityPropagation(**kwargs).fit(S)
    return (len(af.cluster_centers_indices_), zip(graph.nodes(), af.labels_))

def getMincutTree(graph, mincutMethod = ford_fulkerson):
    ''' Construciton of mincut tree as described in 
        "Multi-Terminal Network Flows" - R. E. Gomory and T. C. Hu (http://www.jstor.org/stable/2098881)
    '''
    vertexId = _vertexIdGenerator()
    minCutTree = MinCutTree()
    initialNode = CompoundNode.getInstance(vertexId.next(), graph.nodes())
    _setMincutTreeNode(graph, graph.nodes(), initialNode)
    minCutTree.add_node(initialNode)
    nodeToSplit = initialNode
    while nodeToSplit!=None:
        s, t = nodeToSplit.getRandomPairOfVertices()
        neigboringNodes = []
        reducedGraph = _getReducedGraphForMincutTreeNode(graph, nodeToSplit)
        mincutWeight, (sComponent, tComponent) = mincutMethod(reducedGraph, s, t)
        sCompoundNode = CompoundNode.getInstance(vertexId.next(), sComponent)
        tCompoundNode = CompoundNode.getInstance(vertexId.next(), tComponent)
        for componentNode in [sCompoundNode, tCompoundNode]:
            for v in componentNode.vertices[:]: 
                if type(v) is CompoundNode: 
                    if v in minCutTree[nodeToSplit] and minCutTree[nodeToSplit][v]: neigboringNodes.append((componentNode, v, minCutTree[nodeToSplit][v][CAPACITY]))
                    componentNode.vertices.remove(v)
            _setMincutTreeNode(graph, componentNode.vertices, componentNode)
        minCutTree.splitNode(nodeToSplit, (sCompoundNode, tCompoundNode, mincutWeight), neigboringNodes)
        nodeToSplit = minCutTree.getNextNonSingletonNode()
    graphToReturn = nx.Graph()
    for u, v, data in minCutTree.edges_iter(data=True): graphToReturn.add_edge(u.vertices[0], v.vertices[0], data)
    return graphToReturn

def getMincutTreeForCutClustering(graph, mincutMethod = ford_fulkerson):
    ''' Construciton of efficient mincut tree using heuristic as described in 
        "Graph Clustering and Minimum Cut Trees" - Gary W. Flake, Robert E. Tarjan, Kostas Tsioutsiouliklis (http://www.citeulike.org/user/rocarvaj/article/827986)
    '''
    incidentEdgeWeight = dict([(n,totalIncidentEdgeWeights(graph, n)) for n in graph.nodes_iter()])
    def getNodesSortedByIncidentEdgeWeights(nbunch): return list(zip(*sorted([(n, incidentEdgeWeight[n]) for n in nbunch], key=itemgetter(1), reverse=True))[0])
    vertexId = _vertexIdGenerator()
    minCutTree = MinCutTree()
    initialNode = CompoundNodeForTreeCutClustering.getInstance(vertexId.next(), getNodesSortedByIncidentEdgeWeights(graph.nodes()))
    _setMincutTreeNode(graph, graph.nodes(), initialNode)
    minCutTree.add_node(initialNode)
    nodeToSplit = initialNode
    while nodeToSplit!=None:
        s, t = nodeToSplit.getNextSourceAndSink()
        neigboringNodes = []
        reducedGraph = _getReducedGraphForMincutTreeNode(graph, nodeToSplit)
        mincutWeight, (sComponent, tComponent) = mincutMethod(reducedGraph, s, t)
        sCompoundNode = CompoundNodeForTreeCutClustering.getInstance(vertexId.next(), sComponent)
        tCompoundNode = CompoundNodeForTreeCutClustering.getInstance(vertexId.next(), tComponent)
        for componentNode in [sCompoundNode, tCompoundNode]:
            for v in componentNode.vertices[:]: 
                if type(v) is CompoundNodeForTreeCutClustering: 
                    if v in minCutTree[nodeToSplit] and minCutTree[nodeToSplit][v]: neigboringNodes.append((componentNode, v, minCutTree[nodeToSplit][v][CAPACITY]))
                    componentNode.vertices.remove(v)
            componentNode.vertices = getNodesSortedByIncidentEdgeWeights(componentNode.vertices)
            _setMincutTreeNode(graph, componentNode.vertices, componentNode)
        minCutTree.splitNode(nodeToSplit, (sCompoundNode, tCompoundNode, mincutWeight), neigboringNodes)
        nodeToSplit = minCutTree.getNextNonSingletonNonTNode()
    return minCutTree

class MinCutTree(nx.Graph):
    def getNextNonSingletonNode(self):
        for node in self.nodes():
            if len(node.vertices)>1: return node
    def getNextNonSingletonNonTNode(self):
        for node in self.nodes():
            if len(node.vertices)>1 and CUT_CLUSTERING_T_NODE in node.vertices: return node
    def splitNode(self, nodeToSplit, (split1, split2, mincutWeight), neigboringNodes):
        self.add_edge(split1, split2, capacity=mincutWeight)
        for splitNode, neighbor, capacity in neigboringNodes: self.add_edge(splitNode, neighbor, capacity=capacity)
        self.remove_node(nodeToSplit)

class CompoundNode(str):
    def __init__(self, label): self.value=label
    def getRandomPairOfVertices(self): return sample(self.vertices, 2)
    @staticmethod
    def getInstance(label, vertices): cn = CompoundNode(label); cn.vertices = vertices; return cn
    
class CompoundNodeForTreeCutClustering(CompoundNode):
    def getNextSourceAndSink(self): 
        nextVertexOnTop = self.vertices[0]
        if nextVertexOnTop==CUT_CLUSTERING_T_NODE: nextVertexOnTop = self.vertices[1]
        return nextVertexOnTop, CUT_CLUSTERING_T_NODE
    @staticmethod
    def getInstance(label, vertices): cn = CompoundNodeForTreeCutClustering(label); cn.vertices = vertices; return cn
    
def _vertexIdGenerator(i=0): 
    while True: i+=1; yield 'S%s'%i
def _setMincutTreeNode(graph, nbunch, mincutTreeNode): 
    for n in nbunch: graph.node[n][MINCUT_TREE_NODE]=mincutTreeNode
def _getReducedGraphForMincutTreeNode(graph, mincutTreeNode):
    def getVertexRepresentationInReducedGraph(vertex):
        if graph.node[vertex][MINCUT_TREE_NODE]!= mincutTreeNode: return graph.node[vertex][MINCUT_TREE_NODE];
        else: return vertex
    reducedGraph = nx.Graph()
    for u,v in graph.edges():
        uVertexInReducedGraph, vVertexInReducedGraph = getVertexRepresentationInReducedGraph(u), getVertexRepresentationInReducedGraph(v)
        if reducedGraph.has_edge(uVertexInReducedGraph, vVertexInReducedGraph): reducedGraph[uVertexInReducedGraph][vVertexInReducedGraph][CAPACITY]+=graph[u][v][CAPACITY]
        else: reducedGraph.add_edge(uVertexInReducedGraph, vVertexInReducedGraph, capacity=graph[u][v][CAPACITY])
    return reducedGraph

def clusterUsingMCLClustering(graph, inflation=1.4, **kwargs):
    ''' Uses Markov Cluster Algorithm described in http://micans.org/mcl/.
    '''
    def getClusters(data, inflation=1.4):
        clusters = []
        if data:
            os.environ["PATH"] = os.environ["PATH"]+os.pathsep+'/opt/local/bin'+os.pathsep+'/usr/local/bin'
            mcl_folder = '/tmp/mcl_dir/'
            if not os.path.exists(mcl_folder): os.mkdir(mcl_folder)
            os.chdir(mcl_folder)
            graph_file = open('graph', 'w')
            for edge in data: graph_file.write('%s %s %0.6f\n'%(edge))
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
    return getClusters(edges, inflation=inflation)
    