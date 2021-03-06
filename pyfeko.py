"""
# pyfeko.py v1.1.2
FEKOの計算結果を可視化、サポートするツール群

## UPDATE NOTE

### UPDATE1.1.2

* contour図において、カラーマップ外の色を設定
> `plt.contourf(x, y, Z, interval, alpha=alpha, cmap=cmap, extend="min")`
* cmapは関数の引数から外れた
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def w2db(x):
    """mW -> dB"""
    return 10 * np.log10(x)


def db2w(x):
    """
    dB -> mW
    `df.db2w()` or `db2w(df)`

    ```python
    # TEST
    se = pd.Series(np.arange(10))
    db = se.w2db()
    df = pd.DataFrame({'dBm': db,
                       'watt': db.db2w()})
    print(df)
    ```
    """
    return np.power(10, x / 10)


def v2db(x):
    """V -> dB"""
    return 20 * np.log10(x)


def db2v(x):
    """dB -> V"""
    return np.power(10, x / 20)


def a2comp(mag, arg):
    """
    mag(大きさ)とarg(角度)を引数に、複素数表示で返す。
    引数:
        mag: magnitude
        arg: argument
    戻り値: 複素数表示
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

    * 引数:
        * filename: ファイル名(str型)
        * ram: 電波吸収体反射係数真数。指定しなければ1(=変倍しない)(float型)
    * 戻り値:
        df: 列名が'THETA', 'PHI', 'ET_COMP', 'EP_COMP', 'RCS_dBsm'(* pandas.DataFrame型)
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

    * 引数;
        * column_name:カラムの名前
        * dataframes: データフレームを入れたリスト
    * 戻り値:
        * df.sum(): データフレームの一部だけ取り出したものを
                    ひとつのデータフレームにして、
                    各列を足し算したpandas.Series

    example)
                aa = pd.DataFrame([1,2,3])
                bb = pd.DataFrame([4,5,6])
                sum_rcs(0,[aa,bb])

                # Out:
                0    5  # 1+4
                1    7  # 2+5
                2    9  # 3+6
    """
    df = pd.DataFrame([i[column_name] for i in dataframes])
    return df.sum()


def fine_ticks(tick, deg):
    """
    グラフのticksをいい感じにする

    * 引数:
        * tick: labelに使うリスト(リスト型)
        * deg: labelをdegごとに分割する
    * 戻り値: tickの最大、最小値、degから求めたイイ感じのnp.array

    ```
    # TEST
    #In : for i in range(10,180,10):
              print(fine_ticks(np.arange(181),i))
    #Out :
        [   0.   10.   20.   30.   40.   50.   60.   70.   80.   90.  100.  110.
          120.  130.  140.  150.  160.  170.  180.]
        [   0.   20.   40.   60.   80.  100.  120.  140.  160.  180.]
        [   0.   30.   60.   90.  120.  150.  180.]
        [   0.   45.   90.  135.  180.]
        [   0.   60.  120.  180.]
        [   0.   60.  120.  180.]
        [   0.   90.  180.]
        [   0.   90.  180.]
        [   0.   90.  180.]
        [   0.  180.]
        [   0.  180.]
        [   0.  180.]
        [   0.  180.]
        [   0.  180.]
        [   0.  180.]
        [   0.  180.]
        [   0.  180.]
    ```
    """
    return np.linspace(tick.min(),
                       tick.max(),
                       (tick.max() - tick.min()) / deg + 1)


def plot_contourf(df, title='', xti=30, yti=1, alpha=.75,
                  xlabel='azimuth(deg)', ylabel='elevation(deg)', zlabel='(dBsm)',
                  cmapout='w', cmaphigh=20, cmaplow=0, cmaplevel=100, cmapstep=2, extend='min',
                  fn="Times New Roman", fnsize=12,
                  *args, **kwargs):
    """
    pivotされたデータフレームを引数にcontourfを描く

    * 引数:
        * df: pivotされたデータフレーム
            * x, y, zはdfから計算される
        * title: グラフのタイトル
        * xti, yti: tickの区切り(<n>degごとに分割する)
        * alpha: ヒートマップの透過率
        * xlabel, ylabel, zlabel: ラベル名
        * cmapout: カラーマップ外の値の色
        * cmaphigh, cmaplow, cmaplebel: カラーマップの最大値、最小値、段階
        * cmapstep: 右側に表示されるカラーマップの区切りをいくつごとにするか
        * extend: カラーマップ外の値の色の処理　['neither' | 'both' | 'min' | 'max']
        * fn, fnsize: フォント、フォントサイズ
    * 戻り値: なし
    """
    X = df.columns.values
    Y = df.index.values
    Z = df.values
    x, y = np.meshgrid(X, Y)
    interval = np.linspace(cmaplow, cmaphigh, cmaplevel)  # cmapの段階
    cmap = cm.jet
    cmap.set_under(cmapout, alpha=alpha)  # cmap外の値の色設定
    plt.contourf(x, y, Z, interval, alpha=alpha, cmap=cmap, extend=extend)
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.xticks(fine_ticks(x, xti))  # 30degごと
    plt.yticks(fine_ticks(y, yti))  # 1degごと
    ax = plt.colorbar(ticks=fine_ticks(interval, cmapstep))  # カラーバー2区切りで表示
    ax.set_label(zlabel, fontname=fn)
    plt.title(title, fontsize=fnsize, fontname=fn)
    plt.xlabel(xlabel, fontsize=fnsize, fontname=fn)
    plt.ylabel(ylabel, fontsize=fnsize, fontname=fn)
    plt.grid()


def rolling_around(df, window, mirror=False, min_periods=None, freq=None, center=False,
                   win_type=None, on=None, axis=0, *args, **kwargs):
    """
    * **全周移動平均の作成**
    * mirror=False(デフォルト)のとき、元データを2つ重ねて移動平均をとる。
    > 周回360degのときに使う
    * mirror=Trueのとき、元データをの鏡像を重ねて移動平均をとる。
    > 周回180degのときに使う
    * 移動平均処理後は重ねた分のデータは不必要なので、
      消してインデックスをリセットする。
    > `df.loc[len(df/2):].reset_index()`
    * `pd.DataFrame.rolling`のオプションはすべて使える。
    > 詳細は`pd.DataFrame.rolling?`
    * 引数:
        * df:データフレーム
        * columns:平均処理をするカラム(リスト形式など)
        * window: 平均を行うの区間(int型など)
        * mirror: Trueで鏡像データの作成を行ってから平均化処理
        * 以下はpandasのドキュメント参照
            * min_periods
            * freq
            * center
            * win_type
            * on
            * axis
    * 戻り値: 全周移動平均処理を行ったデータフレーム(pandas.DataFrame型)

    ```python
    # TEST
    n=3
    df = pd.DataFrame(np.arange(n*10).reshape(-1, n), columns=list('abc'))
    window = 2

    a = df.copy()
    normal_rolling_mean = a.rolling(window).mean()
    print('original\n', df)
    print('normal rolling mean\n', normal_rolling_mean)
    print('around rolling mean mirror \n', df.rolling_around(2, mirror=True))
    print('around rolling mean NOT mirror\n',
        df.rolling_around(2, mirror=False))  # mirror=False省略可
    ```
    """
    df_append = df.sort_index(ascending=False) if mirror else df  # mirror=Trueであれば"降順並べ替え"
    df_roll = df_append.append(df, ignore_index=True)  # データをつなげる
    # mirror=Trueなら鏡像データ
    # mirror=Falseなら同じデータがつながる
    f = df_roll.rolling(window, min_periods=min_periods,
                        freq=freq, center=center,
                        win_type=win_type, on=on, axis=axis)
    df_rmean = f.mean()  # 移動平均
    df_rtn = df_rmean.loc[len(df_rmean) / 2:]\
        .reset_index(drop=True)  # rollingしたもの不要な部分切捨てindexをリセット
    return df_rtn


# -----------------------------------------
# メソッドをpd.DataFrame, pd.Seriesに追加
# -----------------------------------------
cs = ('pd.DataFrame', 'pd.Series')
flist = ('rolling_around', 'w2db', 'db2w', 'v2db', 'db2v')
for c in cs:
    for f in flist:
        exec('%s.%s=%s' % (c, f, f))
# 使い方: 区間2の移動平均線 : print(df.rolling_around(2))

# if __name__ == '__main__':
