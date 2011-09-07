'''
Created on Sep 6, 2011

@author: kykamath
'''
import graph_tool.all as gt
import networkx as nx
from numpy.random import seed, random
from scipy.linalg import norm

class XGraph(gt.Graph):
    def __init__(self, g=None, directed=False, prune=False):
        gt.Graph.__init__(self, directed=directed)
        self.node={}; self.edge={};
        self.nodeToNodeIdMap = {}
    def xadd_edge(self, sourceId, targetId):  return self.add_edge(self.node[sourceId], self.node[targetId])
    def xadd_vertex(self, vertexId):
        if vertexId not in self.node: 
            self.node[vertexId]=gt.Graph.add_vertex(self, n=1)
            self.nodeToNodeIdMap[self.node[vertexId]]=vertexId
        return self.node[vertexId]

#g = gt.Graph()
g = XGraph()
vlist = g.xadd_vertex(5)
vlist1 = g.xadd_vertex(6)
vlist2 = []
for v in g.vertices():
    vlist2.append(v)
assert([vlist, vlist1] == vlist2)
print g.num_vertices()
print g.num_edges()
print 'id for', g.node[5], g.nodeToNodeIdMap[vlist]

graph2 = nx.Graph()
graph2.add_edge(1, 2, capacity=10)
graph2.add_edge(2, 3, capacity=13)
graph2.add_edge(3, 1, capacity=12)

def getGraphToolGraphFromNetworkxGraph(nxGraph):
    gtGraph = XGraph()
    capacity = gtGraph.new_edge_property('double')
    for v in nxGraph.nodes_iter(): gtGraph.xadd_vertex(v)
    for u, v, data in nxGraph.edges_iter(data=True): edge = gtGraph.xadd_edge(u, v); capacity[edge] = data['capacity']
    gtGraph.edge_properties['capacity']=capacity
    return gtGraph
    

#seed(42)
#points = random((400, 2)) * 10
#points[0] = [0, 0]
#points[1] = [10, 10]
#g, pos = gt.triangulation(points, type="delaunay")
#g.set_directed(True)
#edges = list(g.edges())
## reciprocate edges
#for e in edges:
#    g.add_edge(e.target(), e.source())
## The capacity will be defined as the inverse euclidian distance
#cap = g.new_edge_property("double")
#for e in g.edges():
#    cap[e] = min(1.0 / norm(pos[e.target()].a - pos[e.source()].a), 10)
#g.edge_properties["cap"] = cap
#g.vertex_properties["pos"] = pos
#g.save("flow-example.xml.gz")
#gt.graph_draw(g, pos=pos, pin=True, penwidth=cap, output="flow-example.pdf")




#graph = XGraph()
#graph.add_edge(graph.add_vertex(), graph.add_vertex())
#graph.add_edge(2, 3, capacity=4)
#graph.add_edge(3, 4, capacity=5)
#graph.add_edge(4, 5, capacity=7)
#graph.add_edge(5, 6, capacity=3)
#graph.add_edge(6, 1, capacity=8)
#graph.add_edge(2, 6, capacity=3)
#graph.add_edge(3, 5, capacity=4)
#graph.add_edge(2, 5, capacity=2)
#graph.add_edge(3, 6, capacity=2)
#graph.add_edge(6, 4, capacity=2)


#g = gt.load_graph("flow-example.xml.gz")
#cap = g.edge_properties["cap"]
#src, tgt = g.vertex(0), g.vertex(1)
#res = gt.boykov_kolmogorov_max_flow(g, src, tgt, cap)
#res.a = cap.a - res.a  # the actual flow
#print [e for e in tgt.in_edges()]
#max_flow = sum(res[e] for e in tgt.in_edges())
#print max_flow
#pos = g.vertex_properties["pos"]
#gt.graph_draw(g, pos=pos, pin=True, penwidth=res, output="example-kolmogorov.pdf")