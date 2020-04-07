import csv
import os
import random
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from numpy import random as nprand

import networkx as nx
from utils import Dataset
from web3 import Web3

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.figsize': (15, 10)})
# get reproducible results
random.seed(123)
nprand.seed(123)

PATH = os.path.dirname(os.getcwd()) + '/images'
WIDTH_IN_INCHES = 10
HEIGHT_IN_INCHES = 6
DPI = 600


REL_FILEPATH = '../../data/transactions.csv'
# REL_FILEPATH = 'test_data.csv'
REL_FILEPATH_EDGES = '../../data/edges.csv'
# REL_FILEPATH_EDGES = 'edges.csv'


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

    recievers = {}
    address_book = {}
    with open('../../data/edges_mapped_s.txt', 'wt') as f:
        no = 0
        for frm, to, total in zip(dataset.data['frm'], dataset.data['to'], dataset.data['total']):
            # convert numpy hashes to string, for some reason some are already strings
            if not type(frm) is str:
                frm = frm.decode('utf-8')
            if not type(to) is str:
                to = to.decode('utf-8')

            # filter out internal transactions
            if frm == to:
                continue

            # replace hashes to numbers for smaller memory usage
            # if frm in address_book:
            #     frm = address_book[frm]
            # else:
            #     no += 1
            #     address_book[frm] = no
            #     frm = no
            # if to in address_book:
            #     to = address_book[to]
            # else:
            #     no += 1
            #     address_book[to] = no
            #     to = no

            if to in recievers:
                recievers[to] += total
            else:
                recievers[to] = total

        percentile = np.percentile(list(recievers.values()), 99.88)
        count = 0
        for frm, to, total in zip(dataset.data['frm'], dataset.data['to'], dataset.data['total']):
            if frm == to:
                continue
            if not type(frm) is str:
                frm = frm.decode('utf-8')
            if not type(to) is str:
                to = to.decode('utf-8')
            # to = address_book[to]
            # frm = address_book[frm]
            if recievers[to] > percentile:
                if (total / recievers[to]) > 0.0025:
                    count += 1
                    f.write('{} {}\n'.format(
                        frm, to))

        print('edges mapped: {}'.format(count))


def main():
    # create_edges()
    # map_edges()

    print('building graph...')
    data_path = '../../data/edges_mapped_s.txt'
    G_social = nx.read_edgelist(data_path)
    pos = nx.spring_layout(G_social, k=0.1)

    smart_contract = []
    normal = []
    web3 = Web3(Web3.HTTPProvider(
        "https://mainnet.infura.io/v3/d373919e558f4fc6826c8bafd737b2b3"))

    print('reading node info...')
    for frm, to in G_social.edges:
        if web3.eth.getCode(Web3.toChecksumAddress(to)) == '0x0':
            normal.append((frm, to))
        else:
            smart_contract.append((frm, to))

    print('drawing graph...')
    plt.rcParams.update({'figure.figsize': (15, 10)})
    nx.draw_networkx(
        G_social,
        pos=pos,
        node_size=0,
        edge_color="#444444",
        edge_list=normal,
        alpha=0.05,
        with_labels=False,
    )
    nx.draw_networkx(
        G_social,
        pos=pos,
        node_size=0,
        edge_color="#80FF00",
        edge_list=smart_contract,
        alpha=0.05,
        with_labels=False,
    )

    print('saving graph...')
    plt.savefig('../images/transactions_cluster.png', dpi=DPI)
    plt.show()


if __name__ == '__main__':
    main()
