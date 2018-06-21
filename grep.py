#!/usr/bin/env python3
from IPython import get_ipython
import pandas as pd
import numpy as np
TOOL = 'grep'


class FekoOut():
    def __init__(self):
        pass

    def frequency(self):
        pattern = ['Freq', '*.out']
        greped = grep(*pattern)
        freq_list = split_list_stings(greped, 'FREQ =')
        return freq_list

    def load(self):
        pass

    def theta(self):
        pass


# Get data in ipython using !grep


def grep(*pattern):
    """ Get only element which contain 'Load1'
    usage:
        pattern = ['-A3', 'Volt', '*.out']
        grep(*pattern)
            or
        grep('-A3', 'Volt' '*.out')
    """
    joined_str = '{} {}'.format(TOOL, ' '.join(pattern))
    grep_str = get_ipython().getoutput(joined_str)
    return grep_str


def split_list_stings(list_strings, delim=None):
    """stlip delim
    default: split multi space
    """
    return [w.split(delim) for w in list_strings]


# Delete unnessesary data in strings


def element(strings):
    """list element transpote to numpy array
    * delete white space
    * delete unnesessary data
    * return numpy array
    """
    el = strings.split()
    al = np.array(el)
    return np.delete(al, [1, 2, 3, 4])


def elements(list_strings):
    """aggregate all element obj in numpy array"""
    return np.array([element(i) for i in list_strings])


# DataFrame calc
def compabs(r, i):
    """abusolute of real and imagine"""
    return np.sqrt(r**2 + i**2)


def antfactor(df, offset):
    """caluclate antenna factor"""
    # compabs fo real & imag
    df['absV(V)'] = compabs(df['realV(V)'], df['imagV(V)'])
    # Antenna factor(E=100dBV)
    df['ant100(dBuV)'] = 20 * np.log10(df['absV(V)']) + offset
    return df


def elem_to_df(array_strings):
    """aggregate pandas DataFrame"""
    index = [i[:-5] for i in array_strings[:, 0]]
    columns = [
        'realV(V)', 'imagV(V)', 'realI(A)', 'imagI(A)', 'realZ(Ohm)',
        'imagZ(Ohm)', 'P(W)'
    ]
    data = array_strings[:, 1:].astype(float)
    df = pd.DataFrame(data=data, index=index, columns=columns)
    df = antfactor(df, 100)
    return df


def main():
    strings = get_ipython().getoutput('rg -A3 Volt *.out')
    list_strings = grep(strings)
    grep_array = elements(list_strings)
    df = elem_to_df(grep_array)
    return df


if __name__ == '__main__':
    main().to_csv('grep_feko.csv')
