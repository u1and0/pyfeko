from time import sleep
from tqdm import tqdm
import pandas as pd
from datetime import datetime


def countdown(n: int):
    """
    n秒待って、経過時間を進捗バーで表す
    """
    pbar = tqdm(range(n))
    for _ in pbar:
        pbar.set_description('Now Waiting %dsec' % n)
        sleep(1)


def countdown_shift(n: str):
    """
    n時間後の日時まで待つ。
    経過時間を進捗バーで表す。

    # TEST
    countdown_shift('1D')
    countdown_shift('5min')
    countdown_shift('1h30min')

    """
    dt = datetime.now()
    endtime = pd.date_range(dt, periods=2, freq=n)  # 現在とn時間経過後の時間を返す
    period = pd.date_range(dt, endtime[-1], freq='S')
    pbar = tqdm(period)
    for _ in pbar:
        wt = period[-1].strftime('%Y/%m/%d %H:%M:%S')
        pbar.set_description('Waiting for %s' % wt)
        sleep(1)


def countdown_end(n: str):
    """
    nの日時まで待つ。
    経過時間を進捗バーで表す。

    引数:
        n: 日付(andas.timestamp型)

    # TEST
    countdown_end('20161106 0924')
    """
    dt = datetime.now()
    period = pd.date_range(start=dt, end=n, freq='S')
    pbar = tqdm(period)
    for _ in pbar:
        wt = period[-1].strftime('%Y/%m/%d %H:%M:%S')
        pbar.set_description('Waiting for %s' % wt)
        sleep(1)


if __name__ == '__main__':
    # countdown(10)
    # countdown_end('20161106 1002')
    # countdown_shift('1D')
    countdown_shift('1min')
    # countdown_shift('1h30min')
    # countdown_shift('1D10min')
