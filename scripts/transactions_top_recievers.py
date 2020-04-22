import csv

import numpy as np

from utils import Dataset
from web3 import Web3

REL_FILEPATH = '../data/top_recievers.csv'
ACCOUNT_INFO = '../data/top_recievers_info.csv'


def main():
    dataset = Dataset(
        REL_FILEPATH, [('to_address', 42), ('total', np.float), ]
    )

    web3 = Web3(Web3.HTTPProvider(
        "https://mainnet.infura.io/v3/d373919e558f4fc6826c8bafd737b2b3"))

    print('reading node info...')
    with open(ACCOUNT_INFO, mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"',)
        file_writer.writerow(['to_address', 'total', 'contract'])
        for to, total in zip(dataset.data['to_address'], dataset.data['total']):
            to = to.decode('utf-8')
            contract = 0 if web3.eth.getCode(
                Web3.toChecksumAddress(to)) == '0x0' else 1
            file_writer.writerow([to, total, contract])


if __name__ == '__main__':
    main()
