'''
cmd: ethereumetl export_blocks_and_transactions --start-block 9581792 --end-block 9782601 \
--provider-uri https://mainnet.infura.io/v3/d373919e558f4fc6826c8bafd737b2b3 \
--blocks-output ../data/blocks.csv --transactions-output ../data/transactions.csv
'''

import os

import matplotlib.pyplot as plt
import pandas as pd

PATH = os.path.dirname(os.getcwd()) + '/images'
width_in_inches = 10
height_in_inches = 6
dots_per_inch = 100

# plot
table = pd.read_csv('xaa')
file = 'transactions_timeseries.png'

table['block_timestamp'] = pd.to_datetime(table['block_timestamp'], unit='s')
# table['gas_price'] = table['gas_price'].apply(lambda x: x/1000000000)
fig, ax = plt.subplots(1, 1)
plt.scatter(x=table['block_timestamp'], y=table['gas_price'], marker='+')
plt.title('Gas limit nach Tag im Monat Maerz')
plt.grid(True)
plt.xlabel('Zeit')
plt.ylabel('gasPrice')
# plt.yscale('log')
fig.set_size_inches(width_in_inches, height_in_inches)
fig.savefig(os.path.join(PATH, file))
