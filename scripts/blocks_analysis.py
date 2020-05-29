import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from utils import Dataset

PATH = os.path.dirname(os.getcwd()) + '/images'
WIDTH_IN_INCHES = 18
HEIGHT_IN_INCHES = 6
DPI = 800


REL_FILEPATH = '../../data/blocks.csv'
# REL_FILEPATH = 'blocks.csv'


def main():
    dataset = Dataset(
        REL_FILEPATH, [('transaction_count', np.float),
                       ('gas_limit', np.float), ('gas_used', np.float), ('timestamp', np.float), ]
    )
    dataset.data['unused_gas'] = list(map(
        lambda x, y: y / x,
        dataset.data['gas_limit'], dataset.data['gas_used']
    ))
    dates = list(map(
        lambda x: datetime.utcfromtimestamp(int(x)),
        dataset.data['timestamp']
    ))
    dataset.standard_analysis()
    dataset.percentiles()
    # plot
    file = 'blocks_unused_gas.png'

    fig, ax = plt.subplots(1, 1)
    plt.hist(
        dataset.data['unused_gas'],
        20,
        density=True,
    )
    plt.grid(True)
    plt.xlabel('percentage of total used gas')
    plt.ylabel('density')
    fig.set_size_inches(WIDTH_IN_INCHES, HEIGHT_IN_INCHES)
    fig.savefig(os.path.join(PATH, file), dpi=DPI)

    file = 'blocks_gas_limit_timeseries.png'

    fig, ax = plt.subplots(1, 1)
    plt.scatter(
        x=dates,
        y=dataset.data['gas_limit'],
        s=0.3,
    )
    plt.title('Block-gasLimit nach Tag im Monat Maerz')
    plt.grid(True)
    plt.xlabel('Zeit')
    plt.ylabel('gasLimit')
    # plt.ylim(9200000, 10001000)
    fig.set_size_inches(WIDTH_IN_INCHES, HEIGHT_IN_INCHES)
    fig.savefig(os.path.join(PATH, file), dpi=DPI)

    file = 'blocks_transactions_per_block.png'

    fig, ax = plt.subplots(1, 1)
    plt.hist(
        dataset.data['transaction_count'],
        60,
        density=True,
    )
    plt.grid(True)
    plt.xlabel('no. of transactions per block')
    plt.ylabel('density')
    fig.set_size_inches(WIDTH_IN_INCHES, HEIGHT_IN_INCHES)
    fig.savefig(os.path.join(PATH, file), dpi=DPI)


if __name__ == '__main__':
    main()
