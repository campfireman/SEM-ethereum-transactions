from subprocess import check_output

import numpy as np


class Dataset():
    '''
    extraction of specific columns to avoid maxining-out memory on big datasets
    '''

    def __init__(self, path, columns, verbose=True):
        self.verbose = verbose
        self.path = path
        self.data = self._extract_data(path, columns)

    @property
    def rows(self) -> int:
        '''
        thanks to https://stackoverflow.com/a/6521584/12653439
        '''
        return int(check_output(["wc", "-l", self.path]).split()[0]) - 1

    def _extract_data(self, path, columns) -> dict:
        result = {}
        indexes = {}
        count = 0
        expected_size = 0

        with open(path, encoding='utf-8') as file:
            header = file.readline().rstrip().split(',')
            expected_size = len(header)
            for c in columns:
                c = c.lower()
                pos = [i for i, x in enumerate(header) if c == x.lower()]
                # check if several headers matched
                if len(pos) > 1:
                    raise ValueError(
                        'column name {} not unique!'.format(c))
                if len(pos) < 1:
                    raise ValueError(
                        'column name {} not found!'.format(c))
                indexes[c] = pos[0]
                result[c] = np.zeros(self.rows)

            if self.verbose:
                print('starting extraction...')

            for line in file:
                line = line.split(',')
                # check for malformed data
                if len(line) != expected_size:
                    raise IOError(
                        'malformed data: line {} not matching exspected size'.format(count))
                for index, pos in indexes.items():
                    result[index][count] = line[pos]
                count += 1

        if self.verbose:
            print('lines read: {}'.format(count))
        return result

    def analyse_aggregates(self, functions) -> None:
        '''
        apply aggregate functions on extracted columns
        '''
        result = {}
        for c, values in self.data.items():
            result[c] = {}
            for name, func in functions.items():
                result[c][name] = func[0](values, *(func[1]), **(func[2]))

        for c, values in result.items():
            print('--- column {} ---'.format(c))
            for name, aggregate in values.items():
                print('{}: {}'.format(name, aggregate))
            print()

    def standard_analysis(self) -> None:
        '''
        median, mean and standarddeviation
        '''
        self.analyse_aggregates({
            'median': (np.median, [], {}),
            'mean': (np.mean, [], {}),
            'std': (np.std, [], {}),
        })

    def percentiles(self) -> None:
        '''
        '''
        self.analyse_aggregates({
            '5th': (np.percentile, [5], {}),
            '10th': (np.percentile, [10], {}),
            '25th': (np.percentile, [25], {}),
            '50th': (np.percentile, [50], {}),
            '75th': (np.percentile, [75], {}),
            '95th': (np.percentile, [95], {}),
        })

    def map(self, column, func) -> None:
        '''
        apply function to all elements in column's array
        '''
        for i, value in enumerate(self.data[column]):
            self.data[column][i] = func(value)
