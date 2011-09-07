# -*- coding: utf-8 -*-
"""
Maximum flow (and minimum cut) algorithms on capacitated graphs.
Using a the code from networkx. Modified the ford_fulkerson method to
get S and T vertices.

http://networkx.lanl.gov/reference/generated/networkx.algorithms.flow.ford_fulkerson.html#networkx.algorithms.flow.ford_fulkerson
"""
from networkx.algorithms.traversal.depth_first_search import dfs_tree

__author__ = """Lo√Øc S√©guin-C. <loicseguin@gmail.com>"""
# Copyright (C) 2010 Lo√Øc S√©guin-C. <loicseguin@gmail.com>
# All rights reserved.
# BSD license.

import networkx as nx

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
            path_capacity = min([auxiliary[u][v][capacity]
                                for u, v in path_edges
                                if capacity in auxiliary[u][v]])
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
            else:
                inf_capacity_flows[(u, v)] += path_capacity

            if auxiliary.has_edge(v, u):
                if capacity in auxiliary[v][u]:
                    auxiliary[v][u][capacity] += path_capacity
            else:
                auxiliary.add_edge(v, u, {capacity: path_capacity})
    S = set([s]+dfs_tree(auxiliary, s).node.keys())
    T = set(G.node.keys()).difference(S)
    return flow_value, (list(S), list(T))
