import csv

import numpy as np

from utils import Dataset
from web3 import Web3

REL_FILEPATH = '../data/no_of_tx.csv'


def main():
    dataset = Dataset(
        REL_FILEPATH, [('no_of_tx', np.int), ('to_address', 42), ]
    )

    web3 = Web3(Web3.HTTPProvider(
        "https://mainnet.infura.io/v3/d373919e558f4fc6826c8bafd737b2b3"))

    print('counting total tx addressed to contracts...')
    total = 0
    for to, no_of_tx in zip(dataset.data['to_address'], dataset.data['no_of_tx']):
        to = to.decode('utf-8')
        contract = 0 if web3.eth.getCode(
            Web3.toChecksumAddress(to)) == '0x0' else 1
        if contract:
            total += no_of_tx
    print('total: {}'.format(total))


if __name__ == '__main__':
    main()
