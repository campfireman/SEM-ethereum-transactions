import os
from datetime import datetime

import matplotlib.pyplot as plt

from utils import Dataset

REL_FILEPATH = '../../data/transactions.csv'
# REL_FILEPATH = 'test_data.csv'

PATH = os.path.dirname(os.getcwd()) + '/images'
WIDTH_IN_INCHES = 10
HEIGHT_IN_INCHES = 6
DPI = 800


def main():
    dataset = Dataset(
        REL_FILEPATH, ['gas_price', 'gas', 'block_timestamp']
    )
    dataset.standard_analysis()

    dataset.map('gas_price', lambda x: x/1000000000)
    dates = list(map(
        lambda x: datetime.utcfromtimestamp(int(x)),
        dataset.data['block_timestamp']
    ))
    # plot
    file = 'transactions_gasprice_timeseries.png'

    fig, ax = plt.subplots(1, 1)
    plt.scatter(
        x=dates,
        y=dataset.data['gas_price'],
        s=0.3,
    )
    plt.grid(True)
    plt.ylim(-10, 900)
    plt.xlabel('Zeit')
    plt.ylabel('gasPrice (GWei)')
    fig.set_size_inches(WIDTH_IN_INCHES, HEIGHT_IN_INCHES)
    fig.savefig(os.path.join(PATH, file), dpi=DPI)


if __name__ == '__main__':
    main()
