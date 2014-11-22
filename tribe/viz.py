# tribe.viz
# Visualization utility for Email social network
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Nov 20 16:28:40 2014 -0500
#
# Copyright (C) 2014 District Data Labs
# For license information, see LICENSE.txt
#
# ID: viz.py [] benjamin@bengfort.com $

"""
Visualization utility for Email social network
"""

##########################################################################
## Imports
##########################################################################

import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

def show_simple_network(nodes=12, prob=0.2, hot=False, triangles=False):
    G = nx.erdos_renyi_graph(nodes, prob)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='#0080C9', node_size=500, linewidths=1.0)
    nx.draw_networkx_edges(G, pos, width=1.0, style='dashed', alpha=0.75)

    if hot:
        center, degree = sorted(G.degree().items(), key=itemgetter(1))[-1]
        nx.draw_networkx_nodes(G, pos, nodelist=[center], node_size=600, node_color="#D9AF0B")

    if triangles:
        edges = G.edges(center)
        other = G.edges(nx.all_neighbors(G, center))

        nx.draw_networkx_edges(G, pos, edgelist=other, style='solid')
        nx.draw_networkx_edges(G, pos, edgelist=edges, style='solid', edge_color='#009E2D', width=2.0)

    plt.axis('off')
    plt.show()

    return G
