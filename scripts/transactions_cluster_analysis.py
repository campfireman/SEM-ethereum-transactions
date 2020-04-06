import csv
import os
import random
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy import random as nprand

import networkx as nx
import networkx.algorithms.community as nxcom
from utils import Dataset

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.figsize': (15, 10)})
# get reproducible results
random.seed(123)
nprand.seed(123)

PATH = os.path.dirname(os.getcwd()) + '/images'
WIDTH_IN_INCHES = 10
HEIGHT_IN_INCHES = 6
DPI = 800


REL_FILEPATH = '../../data/transactions.csv'
# REL_FILEPATH = 'test_data.csv'
REL_FILEPATH_EDGES = '../../data/edges.csv'
# REL_FILEPATH_EDGES = 'edges.csv'


def set_node_community(G, communities):
    '''Add community to node attributes'''
    for c, v_c in enumerate(communities):
        for v in v_c:
            # Add 1 to save 0 for external edges
            G.nodes[v]['community'] = c + 1


def set_edge_community(G):
    '''Find internal edges and add their community to their attributes'''
    for v, w, in G.edges:
        if G.nodes[v]['community'] == G.nodes[w]['community']:
            # Internal edge, mark with community
            G.edges[v, w]['community'] = G.nodes[v]['community']
        else:
            # External edge, mark as 0
            G.edges[v, w]['community'] = 0


def get_color(i, r_off=1, g_off=1, b_off=1):
    '''Assign a color to a vertex.'''
    r0, g0, b0 = 0, 0, 0
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 3) % n) / (n - 1)
    g = low + span * (((i + g_off) * 5) % n) / (n - 1)
    b = low + span * (((i + b_off) * 7) % n) / (n - 1)
    return (r, g, b)


def create_edges():
    dataset = Dataset(
        REL_FILEPATH, [
            ('from_address', 42),
            ('to_address', 42),
            ('value', np.float), ('gas_price', np.float), ('gas', np.float)
        ]
    )
    data = dataset.data
    connections = {}

    for (frm, to, value, gas_price, gas) in zip(data['from_address'], data['to_address'], data['value'], data['gas_price'], data['gas']):
        total = (value + (gas_price * gas)) / 10 ** 18
        if frm in connections:
            if to in connections[frm]:
                connections[frm][to]['total'] += total
                connections[frm][to]['count'] += 1
            else:
                connections[frm] = {
                    to: {
                        'total': total,
                        'count': 0
                    }
                }
        else:
            connections[frm] = {
                to: {
                    'total': total,
                    'count': 0
                }
            }

    with open('../../data/edges.csv', 'wt') as f:
        csv_writer = csv.writer(f)
        header = ['frm', 'to', 'total', 'count']
        csv_writer.writerow(header)  # write header

        for frm, dest in connections.items():
            for to, values in dest.items():
                for total, count in values:
                    if not type(frm) is str:
                        frm = frm.decode('utf-8')
                    if not type(to) is str:
                        to = to.decode('utf-8')
                    csv_writer.writerow(
                        (frm, to, total, count))


def map_edges():
    dataset = Dataset(
        REL_FILEPATH_EDGES,
        [
            ('frm', 42), ('to', 42), ('total', np.float)]
    )
    no = 1
    address_book = {}
    with open('../../data/edges_mapped_s.txt', 'wt') as f:
        for frm, to, total in zip(dataset.data['frm'], dataset.data['to'], dataset.data['total']):
            if total > 5:
                if not type(frm) is str:
                    frm = frm.decode('utf-8')
                if not type(to) is str:
                    to = to.decode('utf-8')
                if frm in address_book:
                    frm = address_book[frm]
                else:
                    no += 1
                    address_book[frm] = no
                    frm = no

                if to in address_book:
                    to = address_book[to]
                else:
                    no += 1
                    address_book[to] = no
                    to = no

                f.write('{} {}\n'.format(
                    frm, to))


def main():
    # create_edges()
    map_edges()
    # dataset = Dataset(
    #     REL_FILEPATH_EDGES,
    #     [
    #         ('frm', 42), ('to', 42),
    #         ('total', np.float)]
    # )
    # # dataset.standard_analysis()
    # data = dataset.data
    # DG = nx.DiGraph()
    # for frm, to, total in zip(data['frm'], data['to'], data['total']):
    #     if total > 170:
    #         DG.add_edge(frm, to)
    # print(edges)

    # # DG.add_weighted_edges_from(edges)
    # pos = nx.layout.spring_layout(DG)

    # M = DG.number_of_edges()
    # edge_colors = range(2, M + 2)

    # nodes = nx.draw_networkx_nodes(
    #     DG, pos, node_size=6, node_color="blue")
    # edges = nx.draw_networkx_edges(
    #     DG,
    #     pos,
    #     arrowstyle="->",
    #     arrowsize=6,
    #     width=2,
    # )

    # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
    # pc.set_array(edge_colors)
    # plt.colorbar(pc)

    # ax = plt.gca()
    # ax.set_axis_off()
    # plt.show()
    data_path = '../../data/edges_mapped_s.txt'
    # data_path = './facebook_combined.txt'
    print('building graph...')
    G_social = nx.read_edgelist(data_path)

    pos = nx.spring_layout(G_social, k=0.1)
    plt.rcParams.update({'figure.figsize': (15, 10)})
    # nx.draw_networkx(
    #     G_social,
    #     pos=pos,
    #     node_size=0,
    #     edge_color="#444444",
    #     alpha=0.05,
    #     with_labels=False)

    communities = sorted(nxcom.greedy_modularity_communities(
        G_social), key=len, reverse=True)
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams.update({'figure.figsize': (15, 10)})
    plt.style.use('dark_background')

    # Set node and edge communities
    set_node_community(G_social, communities)
    set_edge_community(G_social)

    # Set community color for internal edges
    external = [(v, w)
                for v, w in G_social.edges if G_social.edges[v, w]['community'] == 0]
    internal = [(v, w)
                for v, w in G_social.edges if G_social.edges[v, w]['community'] > 0]
    internal_color = ["black" for e in internal]
    node_color = [get_color(G_social.nodes[v]['community'])
                  for v in G_social.nodes]
    # external edges
    nx.draw_networkx(
        G_social,
        pos=pos,
        node_size=0,
        edgelist=external,
        edge_color="silver",
        node_color=node_color,
        alpha=0.2,
        with_labels=False)
    # internal edges
    nx.draw_networkx(
        G_social, pos=pos,

        edgelist=internal,
        edge_color=internal_color,
        node_color=node_color,
        alpha=0.05,
        with_labels=False)
    print('saving graph...')
    plt.savefig('../images/transactions_cluster.png', dpi=DPI)
    plt.show()


if __name__ == '__main__':
    main()
