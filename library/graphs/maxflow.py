# -*- coding: utf-8 -*-
"""
Maximum flow (and minimum cut) algorithms on capacitated graphs.
"""
from networkx.algorithms.components.connected import connected_components

__author__ = """Loïc Séguin-C. <loicseguin@gmail.com>"""
# Copyright (C) 2010 Loïc Séguin-C. <loicseguin@gmail.com>
# All rights reserved.
# BSD license.

import networkx as nx
from operator import itemgetter
from itertools import groupby, product

__all__ = ['ford_fulkerson',
           'ford_fulkerson_flow',
           'max_flow',
           'min_cut']


def _create_auxiliary_digraph(G, capacity='capacity'):
    """Initialize an auxiliary digraph and dict of infinite capacity
    edges for a given graph G.
    Ignore edges with capacity <= 0.
    """
    auxiliary = nx.DiGraph()
    inf_capacity_flows = {}

    if nx.is_directed(G):
        for edge in G.edges(data = True):
            if capacity in edge[2]:
                if edge[2][capacity] > 0:
                    auxiliary.add_edge(*edge)
            else:
                auxiliary.add_edge(*edge)
                inf_capacity_flows[(edge[0], edge[1])] = 0
    else:
        for edge in G.edges(data = True):
            if capacity in edge[2]:
                if edge[2][capacity] > 0:
                    auxiliary.add_edge(*edge)
                    auxiliary.add_edge(edge[1], edge[0], edge[2])
            else:
                auxiliary.add_edge(*edge)
                auxiliary.add_edge(edge[1], edge[0], edge[2])
                inf_capacity_flows[(edge[0], edge[1])] = 0
                inf_capacity_flows[(edge[1], edge[0])] = 0

    return auxiliary, inf_capacity_flows


def _create_flow_dict(G, H, inf_capacity_flows, capacity='capacity'):
    """Creates the flow dict of dicts on G corresponding to the
    auxiliary digraph H and infinite capacity edges flows
    inf_capacity_flows.
    """
    flow = dict([(u, {}) for u in G])

    if G.is_directed():
        for u, v in G.edges_iter():
            if H.has_edge(u, v):
                if capacity in G[u][v]:
                    flow[u][v] = max(0, G[u][v][capacity] - H[u][v][capacity])
                elif G.has_edge(v, u) and not capacity in G[v][u]:
                    flow[u][v] = max(0, inf_capacity_flows[(u, v)] -
                                     inf_capacity_flows[(v, u)])
                else:
                    flow[u][v] = max(0, H[v].get(u, {}).get(capacity, 0) -
                                     G[v].get(u, {}).get(capacity, 0))
            else:
                flow[u][v] = G[u][v][capacity]

    else: # undirected
        for u, v in G.edges_iter():
            if H.has_edge(u, v):
                if capacity in G[u][v]:
                    flow[u][v] = abs(G[u][v][capacity] - H[u][v][capacity])
                else:
                    flow[u][v] = abs(inf_capacity_flows[(u, v)] -
                                     inf_capacity_flows[(v, u)])
            else:
                flow[u][v] = abs(G[u][v][capacity] - H[v][u][capacity])
            flow[v][u] = flow[u][v]

    return flow

uniqueString = '_%$^%$^%$^$%^$%^_'
def edgeLabel(u, v): return uniqueString.join(sorted([str(u),str(v)]))
def retrieveVertexFromLabel(label): return label.split(uniqueString)

def _getGraphComponentsAfterFlow(G, potentialEdgesToRemove):

#    for edgeSet in list(product(*potentialEdgesToRemove)):
#        tempGraph = G.subgraph(G.nodes()).copy()
#        for u, v in edgeSet: tempGraph.remove_edge(u, v)
#        print edgeSet
#        components = connected_components(tempGraph)
#        print components, len(components)
#        if len(components)==2: return components 
    
    tempGraph = G.subgraph(G.nodes()).copy()
    for edge in potentialEdgesToRemove: 
        tempGraph.remove_edge(*edge)
        components = connected_components(tempGraph)
        if len(components)==2: return components         
        
        
#        print potentialEdgesToRemove
#        print list(product(*potentialEdgesToRemove))
#    for u, v in G.edges_iter(): 
#        tempGraph.add_node(u), tempGraph.add_node(v)
#        if edgeLabel(u, v) not in edgesRemoved: tempGraph.add_edge(u, v)
#    return connected_components(tempGraph)
    

def ford_fulkerson(G, s, t, capacity='capacity'):
    """Find a maximum single-commodity flow using the Ford-Fulkerson
    algorithm.
    
    This algorithm uses Edmonds-Karp-Dinitz path selection rule which
    guarantees a running time of O(nm^2) for n nodes and m edges.


    Parameters
    ----------
    G : NetworkX graph
        Edges of the graph are expected to have an attribute called
        'capacity'. If this attribute is not present, the edge is
        considered to have infinite capacity.

    s : node
        Source node for the flow.

    t : node
        Sink node for the flow.

    capacity: string
        Edges of the graph G are expected to have an attribute capacity
        that indicates how much flow the edge can support. If this
        attribute is not present, the edge is considered to have
        infinite capacity. Default value: 'capacity'.

    Returns
    -------
    flow_value : integer, float
        Value of the maximum flow, i.e., net outflow from the source.

    flow_dict : dictionary
        Dictionary of dictionaries keyed by nodes such that
        flow_dict[u][v] is the flow edge (u, v).

    Raises
    ------
    NetworkXError
        The algorithm does not support MultiGraph and MultiDiGraph. If
        the input graph is an instance of one of these two classes, a
        NetworkXError is raised.

    NetworkXUnbounded
        If the graph has a path of infinite capacity, the value of a 
        feasible flow on the graph is unbounded above and the function
        raises a NetworkXUnbounded.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.DiGraph()
    >>> G.add_edge('x','a', capacity=3.0)
    >>> G.add_edge('x','b', capacity=1.0)
    >>> G.add_edge('a','c', capacity=3.0)
    >>> G.add_edge('b','c', capacity=5.0)
    >>> G.add_edge('b','d', capacity=4.0)
    >>> G.add_edge('d','e', capacity=2.0)
    >>> G.add_edge('c','y', capacity=2.0)
    >>> G.add_edge('e','y', capacity=3.0)
    >>> flow, F = nx.ford_fulkerson(G, 'x', 'y')
    >>> flow
    3.0
    """
    if G.is_multigraph():
        raise nx.NetworkXError(
                'MultiGraph and MultiDiGraph not supported (yet).')

    auxiliary, inf_capacity_flows = _create_auxiliary_digraph(G,
                                                        capacity=capacity)
    flow_value = 0   # Initial feasible flow.
    potentialEdgesToRemove = []

    # As long as there is an (s, t)-path in the auxiliary digraph, find
    # the shortest (with respect to the number of arcs) such path and
    # augment the flow on this path.
    while True:
        try:
            path_nodes = nx.bidirectional_shortest_path(auxiliary, s, t)
        except nx.NetworkXNoPath:
            break

        # Get the list of edges in the shortest path.
        path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))

        # Find the minimum capacity of an edge in the path.
        try:
            pathData = [((u, v), auxiliary[u][v][capacity]) 
                                 for u, v in path_edges 
                                 if capacity in auxiliary[u][v]]
            edges_by_path_capacity = dict([(u, list(v)) for u, v in groupby(pathData, key=itemgetter(1))])
            _, path_capacity = min(pathData, key=itemgetter(1))
#            minEdgePath = None
#            print edges_by_path_capacity
#            if len(edges_by_path_capacity[path_capacity])>1: minEdgePath = edges_by_path_capacity[path_capacity][0][0]
#            else: minEdgePath = edges_by_path_capacity[path_capacity][0][0]
#            print edges_by_path_capacity
#            print path_capacity, edges_by_path_capacity[path_capacity]
#            print [i[0] for i in edges_by_path_capacity[path_capacity]]
#            potentialEdgesToRemove.append((len([i[0] for i in edges_by_path_capacity[path_capacity]]), [i[0] for i in edges_by_path_capacity[path_capacity]]))
#            print '****', minEdgePath, path_capacity
        except ValueError: 
            # path of infinite capacity implies no max flow
            raise nx.NetworkXUnbounded(
                    "Infinite capacity path, flow unbounded above.")
        
        flow_value += path_capacity

        # Augment the flow along the path.
        for u, v in path_edges:
            edge_attr = auxiliary[u][v]
            if capacity in edge_attr:
                edge_attr[capacity] -= path_capacity
                if edge_attr[capacity] == 0:
                    auxiliary.remove_edge(u, v)
#                    print u, v
                    potentialEdgesToRemove.append((u, v))
            else:
                inf_capacity_flows[(u, v)] += path_capacity

            if auxiliary.has_edge(v, u):
                if capacity in auxiliary[v][u]:
                    auxiliary[v][u][capacity] += path_capacity
            else:
                auxiliary.add_edge(v, u, {capacity: path_capacity})
    
    flow_dict = _create_flow_dict(G, auxiliary, inf_capacity_flows,
                                  capacity=capacity)
#    potentialEdgesToRemove = [i[1] for i in sorted(potentialEdgesToRemove, key=itemgetter(0))]
    componentsAfterFlow = _getGraphComponentsAfterFlow(G, potentialEdgesToRemove)
    return flow_value, flow_dict, componentsAfterFlow


def ford_fulkerson_flow(G, s, t, capacity='capacity'):
    """Return a maximum flow for a single-commodity flow problem.

    Parameters
    ----------
    G : NetworkX graph
        Edges of the graph are expected to have an attribute called
        'capacity'. If this attribute is not present, the edge is
        considered to have infinite capacity.

    s : node
        Source node for the flow.

    t : node
        Sink node for the flow.

    capacity: string
        Edges of the graph G are expected to have an attribute capacity
        that indicates how much flow the edge can support. If this
        attribute is not present, the edge is considered to have
        infinite capacity. Default value: 'capacity'.

    Returns
    -------
    flow_dict : dictionary
        Dictionary of dictionaries keyed by nodes such that
        flow_dict[u][v] is the flow edge (u, v).

    Raises
    ------
    NetworkXError
        The algorithm does not support MultiGraph and MultiDiGraph. If
        the input graph is an instance of one of these two classes, a
        NetworkXError is raised.

    NetworkXUnbounded
        If the graph has a path of infinite capacity, the value of a 
        feasible flow on the graph is unbounded above and the function
        raises a NetworkXUnbounded.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.DiGraph()
    >>> G.add_edge('x','a', capacity=3.0)
    >>> G.add_edge('x','b', capacity=1.0)
    >>> G.add_edge('a','c', capacity=3.0)
    >>> G.add_edge('b','c', capacity=5.0)
    >>> G.add_edge('b','d', capacity=4.0)
    >>> G.add_edge('d','e', capacity=2.0)
    >>> G.add_edge('c','y', capacity=2.0)
    >>> G.add_edge('e','y', capacity=3.0)
    >>> F = nx.ford_fulkerson_flow(G, 'x', 'y')
    >>> for u, v in G.edges_iter():
    ...     print('(%s, %s) %.2f' % (u, v, F[u][v]))
    ... 
    (a, c) 2.00
    (c, y) 2.00
    (b, c) 0.00
    (b, d) 1.00
    (e, y) 1.00
    (d, e) 1.00
    (x, a) 2.00
    (x, b) 1.00
    """
    return ford_fulkerson(G, s, t, capacity=capacity)[1]


def max_flow(G, s, t, capacity='capacity'):
    """Find the value of a maximum single-commodity flow.
    
    Parameters
    ----------
    G : NetworkX graph
        Edges of the graph are expected to have an attribute called
        'capacity'. If this attribute is not present, the edge is
        considered to have infinite capacity.

    s : node
        Source node for the flow.

    t : node
        Sink node for the flow.

    capacity: string
        Edges of the graph G are expected to have an attribute capacity
        that indicates how much flow the edge can support. If this
        attribute is not present, the edge is considered to have
        infinite capacity. Default value: 'capacity'.

    Returns
    -------
    flow_value : integer, float
        Value of the maximum flow, i.e., net outflow from the source.

    Raises
    ------
    NetworkXError
        The algorithm does not support MultiGraph and MultiDiGraph. If
        the input graph is an instance of one of these two classes, a
        NetworkXError is raised.

    NetworkXUnbounded
        If the graph has a path of infinite capacity, the value of a 
        feasible flow on the graph is unbounded above and the function
        raises a NetworkXUnbounded.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.DiGraph()
    >>> G.add_edge('x','a', capacity=3.0)
    >>> G.add_edge('x','b', capacity=1.0)
    >>> G.add_edge('a','c', capacity=3.0)
    >>> G.add_edge('b','c', capacity=5.0)
    >>> G.add_edge('b','d', capacity=4.0)
    >>> G.add_edge('d','e', capacity=2.0)
    >>> G.add_edge('c','y', capacity=2.0)
    >>> G.add_edge('e','y', capacity=3.0)
    >>> flow = nx.max_flow(G, 'x', 'y')
    >>> flow
    3.0
    """
    return ford_fulkerson(G, s, t, capacity=capacity)[0]


def min_cut(G, s, t, capacity='capacity'):
    """Compute the value of a minimum (s, t)-cut.

    Use the max-flow min-cut theorem, i.e., the capacity of a minimum
    capacity cut is equal to the flow value of a maximum flow.

    Parameters
    ----------
    G : NetworkX graph
        Edges of the graph are expected to have an attribute called
        'capacity'. If this attribute is not present, the edge is
        considered to have infinite capacity.

    s : node
        Source node for the flow.

    t : node
        Sink node for the flow.

    capacity: string
        Edges of the graph G are expected to have an attribute capacity
        that indicates how much flow the edge can support. If this
        attribute is not present, the edge is considered to have
        infinite capacity. Default value: 'capacity'.

    Returns
    -------
    cutValue : integer, float
        Value of the minimum cut.
    
    Raises
    ------
    NetworkXUnbounded
        If the graph has a path of infinite capacity, all cuts have
        infinite capacity and the function raises a NetworkXError.
    
    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.DiGraph()
    >>> G.add_edge('x','a', capacity = 3.0)
    >>> G.add_edge('x','b', capacity = 1.0)
    >>> G.add_edge('a','c', capacity = 3.0)
    >>> G.add_edge('b','c', capacity = 5.0)
    >>> G.add_edge('b','d', capacity = 4.0)
    >>> G.add_edge('d','e', capacity = 2.0)
    >>> G.add_edge('c','y', capacity = 2.0)
    >>> G.add_edge('e','y', capacity = 3.0)
    >>> nx.min_cut(G, 'x', 'y')
    3.0
    """

    try:
        return ford_fulkerson(G, s, t, capacity=capacity)[0]
    except nx.NetworkXUnbounded:
        raise nx.NetworkXUnbounded(
                "Infinite capacity path, no minimum cut.")

