import networkx as nx
import matplotlib.pyplot as plt
from random import sample
from graphs.maxflow import ford_fulkerson

MINCUT_TREE_NODE = 'mincut_tree_node'
CAPACITY = 'capacity'

def plot(graph, **kwargs):
    pos=kwargs.get('pos', nx.spring_layout(graph))
    if kwargs.get('draw_edge_labels', False): edge_labels=nx.draw_networkx_edge_labels(graph,pos)
    else: edge_labels=[]
    nx.draw(graph, pos, edge_labels=edge_labels, **kwargs)
    plt.show()

def getMincutTree(graph, mincutMethod = ford_fulkerson):
    ''' Construciton of mincut tree as described in 
        "Multi-Terminal Network Flows" - R. E. Gomory and T. C. Hu (http://www.jstor.org/stable/2098881)
    '''
    def vertexIdGenerator(i=0): 
        while True: i+=1; yield 'S%s'%i
    def setMincutTreeNode(nbunch, mincutTreeNode): 
        for n in nbunch: graph.node[n][MINCUT_TREE_NODE]=mincutTreeNode
    def getReducedGraphForMincutTreeNode(mincutTreeNode):
        def getVertexRepresentationInReducedGraph(vertex):
            if graph.node[vertex][MINCUT_TREE_NODE]!= mincutTreeNode: return graph.node[vertex][MINCUT_TREE_NODE];
            else: return vertex
        reducedGraph = nx.Graph()
        for u,v in graph.edges():
            uVertexInReducedGraph, vVertexInReducedGraph = getVertexRepresentationInReducedGraph(u), getVertexRepresentationInReducedGraph(v)
            if reducedGraph.has_edge(uVertexInReducedGraph, vVertexInReducedGraph): reducedGraph[uVertexInReducedGraph][vVertexInReducedGraph][CAPACITY]+=graph[u][v][CAPACITY]
            else: reducedGraph.add_edge(uVertexInReducedGraph, vVertexInReducedGraph, capacity=graph[u][v][CAPACITY])
        return reducedGraph
            
    vertexId = vertexIdGenerator()
    minCutTree = MinCutTree()
    initialNode = CompoundNode.getInstance(vertexId.next(), graph.nodes())
    setMincutTreeNode(graph.nodes(), initialNode)
    minCutTree.add_node(initialNode)
    nodeToSplit = initialNode
    
    while nodeToSplit!=None:
        print '\n\n\n'
        s, t = nodeToSplit.getRandomPairOfVertices()
#        s, t = 6,1
#        print s, t
        neigboringNodes = []
        reducedGraph = getReducedGraphForMincutTreeNode(nodeToSplit)
        print [(n, n.vertices) for n in reducedGraph.nodes() if type(n) is CompoundNode ]
#        a,b,c = mincutMethod(reducedGraph, s, t)
        print s, t
        mincutWeight, _, (sComponent, tComponent) = mincutMethod(reducedGraph, s, t)
        sCompoundNode = CompoundNode.getInstance(vertexId.next(), sComponent)
        tCompoundNode = CompoundNode.getInstance(vertexId.next(), tComponent)
        for componentNode in [sCompoundNode, tCompoundNode]:
            for v in componentNode.vertices[:]: 
                if type(v) is CompoundNode: 
                    if v in minCutTree[nodeToSplit] and minCutTree[nodeToSplit][v]: neigboringNodes.append((componentNode, v, minCutTree[nodeToSplit][v][CAPACITY]))
                    componentNode.vertices.remove(v)
            setMincutTreeNode(componentNode.vertices, componentNode)
        minCutTree.splitNode(nodeToSplit, (sCompoundNode, tCompoundNode, mincutWeight), neigboringNodes)
#        exit()
        nodeToSplit = minCutTree.getNextNonSingletonNode()
    
    graphToReturn = nx.Graph()
    for u, v, data in minCutTree.edges_iter(data=True): graphToReturn.add_edge(u.vertices[0], v.vertices[0], data)
    return graphToReturn

class MinCutTree(nx.Graph):
    def getNextNonSingletonNode(self):
        for node in self.nodes():
            if len(node.vertices)>1: return node
    def splitNode(self, nodeToSplit, (split1, split2, mincutWeight), neigboringNodes):
        self.add_edge(split1, split2, capacity=mincutWeight)
        for splitNode, neighbor, capacity in neigboringNodes: self.add_edge(splitNode, neighbor, capacity=capacity)
        self.remove_node(nodeToSplit)

class CompoundNode(str):
    def __init__(self, label): self.value=label#; self.metaInfo = {}
    def getRandomPairOfVertices(self): return sample(self.vertices, 2)
    @staticmethod
    def getInstance(label, vertices): cn = CompoundNode(label); cn.vertices = vertices; return cn
    
    