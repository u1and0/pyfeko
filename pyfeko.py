"""
FEKOの計算結果を
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def w2db(x):
    """mW -> dB"""
    return 10 * np.log10(x)


def db2w(x):
    """dB -> mW"""
    return np.power(10, x/10)


def v2db(x):
    """V -> dB"""
    return 20 * np.log10(x)


def db2v(x):
    """dB -> V"""
    return np.power(10, x/20)


def a2comp(mag, arg):
    """
    mag(大きさ)とarg(角度)を引数に、複素数表示で返す。
    引数:
        mag: magnitude
        arg: argument
    戻り値:
             mag * (np.cos(np.radians(arg)) + np.sin(np.radians(arg)) * 1j): 複素数表示
    """
    return mag * (np.cos(np.radians(arg)) + np.sin(np.radians(arg)) * 1j)

    
def rcs_total(Etheta, Ephi, source_power):
    """
    引数：
        Etheta, Ephi: 電界強度(複素数)
        source_power: ソースの電界強度[V/m]。普通は1？outファイルやfrkoのファイル参照
    戻り値: 単位ソースパワーあたりのEthetaとEphiの絶対値を出して4pi掛けた値
    """
    return 4 * np.pi * (((np.abs(Etheta))**2 + (np.abs(Ephi))**2) / source_power)


def import_data(filename: str):
    """
    FEKOの.outファイルをpandas DataFrame形式にして返す

    引数:
        filename: ファイル名(str型)
    戻り値:
        df: 列名がtheta phi, (pandas.DataFrame型)
    """
    ar = []
    dataline = False
    for line in open(filename, "r"):
        if line[3:8] == "THETA":  # 3-8文字目に"THETA"を含むラインはデータが含まれている
            dataline = True
            continue
        if dataline:
            data = line.split()
            ar.append([float(data[0]),
                              float(data[1]),
                              w2db(float(data[6]))])  # RCS値をdBm表示
            dataline = False
    print("Import data completed")
    df = pd.DataFrame(ar, columns=["THETA", "PHI", "RCS_dBsm"])
    del ar
    return df


def import_data_comp(filename: str, ram=1):
    """
    FEKOの.outファイルをpandas DataFrame形式にして返す

    引数:
        filename: ファイル名(str型)
        ram: 電波吸収体反射係数真数。指定しなければ1(=変倍しない)(float型)
    戻り値:
        df: 列名が'THETA', 'PHI', 'ET_COMP', 'EP_COMP', 'RCS_dBsm'(pandas.DataFrame型)
    """
    ar = []
    dataline = False
    for line in open(filename, "r"):
        if line[3:8] == "THETA":  # 3-8文字目に"THETA"を含むラインはデータが含まれている
            dataline = True
            continue
        if dataline:
            data = line.split()
            et_mag = float(data[2]) * ram
            et_ph = float(data[3])
            ep_mag = float(data[4]) * ram
            ep_ph = float(data[5])
            et_comp = a2comp(et_mag, et_ph)  # 複素数表示
            ep_comp = a2comp(ep_mag, ep_ph)
            rcs_w = rcs_total(et_comp, ep_comp, 1)  # 分母の'1'は計算時に指定したソースパワー
            rcs = w2db(rcs_w)
            ar.append([float(data[0]) - 90,
                             float(data[1]),
                             et_comp,
                             ep_comp,
                             rcs])  # RCS値をdBm表示
            dataline = False
    print("Import data completed")
    df = pd.DataFrame(ar)
    df.columns = ["THETA", "PHI", "ET_COMP", "EP_COMP", "RCS_dBsm"]
    return df


def sumdf(column_name, dataframes: list):
    """
    引数にしたデータフレームの特定のカラムを足し算してデータフレームとして返す。
    
    引数;
        column_name:カラムの名前
        dataframes: データフレームを入れたリスト
    戻り値:
        df.sum(): データフレームの一部だけ取り出したものを
                    ひとつのデータフレームにして
                    各列を足し算したもの
                    
    example)
                aa = pd.DataFrame([1,2,3])
                bb = pd.DataFrame([4,5,6])
                sum_rcs(0,[aa,bb])
                
                # Out: 
                0    5
                1    7
                2    9
    """
    df = pd.DataFrame([i[column_name] for i in dataframes])
    return df.sum()




from time import clock
from itertools import chain
#if __name__ == '__main__':
