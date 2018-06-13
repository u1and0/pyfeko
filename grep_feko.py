#!/usr/bin/env python3
from IPython import get_ipython
import pandas as pd
import numpy as np

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


# Get data in ipython using !grep
def get_data(strings):
    """ Get only element which contain 'Load1'

    args
        * strings: get from grep out file
    usage:
        strings = get_ipython().getoutput('rg -A3 Volt *.out ')
        get_data(strings)

            or

        get_data(!rg -A3 Volt *.out)
    """
    return [i for i in strings if 'Load1' in i]


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
    """com numpy array"""
    return np.array([element(i) for i in list_strings])


def elem_to_df(array_strings):
    index = array_strings[:, 0]
    columns = [
        'realV(V)', 'imagV(V)', 'realI(A)', 'imagI(A)', 'realZ(Ohm)',
        'imagZ(Ohm)', 'P(W)'
    ]
    data = array_strings[:, 1:].astype(float)
    df = pd.DataFrame(data=data, index=index, columns=columns)
    df = antfactor(df, 100)
    return df


if __name__ == '__main__':
    grep = get_ipython().getoutput('rg -A3 Volt *.out')
    list_strings = get_data(grep)
    grep_array = elements(list_strings)
    df = elem_to_df(grep_array)
    df.to_csv('test_file.csv')
