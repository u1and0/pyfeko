"""
## runtime_scheduler ver1.0

__USAGE__
`python runfeko.py <ファイル名の正規表現> <待ち時間>`

```
$ 正規表現でファイル名を入力してください。>>> ../*dat
$ 何秒後に実行？ / 入力なし->Enterで直ちに実行 >>>
$ echo ..\data.dat foo
$ echo ..\mat.dat foo
$ 以上のコマンドを実行します。よろしいですか？ y/n? >>>y
--
yesが入力されました。処理を続行します。

  0%|
                                                           | 0/2 [00:00<?, ?it/s] 実行サイクル: 1/2
実行コマンド:  echo ..\data.dat foo
..\data.dat foo
開始時刻:  2016-11-06 07:58:29.763531
終了時刻:  2016-11-06 07:58:29.887614
実行時間:  0:00:00.124083
 50%|███████████████████████████████
███████████████████████
                                   | 1/2 [00:00<00:00,  7.81it/s] 実行サイクル: 2/2
実行コマンド:  echo ..\mat.dat foo
..\mat.dat foo
開始時刻:  2016-11-06 07:58:29.892617
終了時刻:  2016-11-06 07:58:30.020703
実行時間:  0:00:00.128086
100%|███████████████████████████████
██████████████████████████████████
██████████████████████████████████
█████████| 2/2 [00:00<00:00,  7.75it/s]
```

__INTRODUCTION__
cmdに渡すコマンド
`runfeko <file> -np 16`
を作り出して、FEKOを実行する。

__ACTION__
globで正規表現に基づいたファイル名を
commandという変数に格納していく。
変数commnandにはあらかじめ`runtime <filename> -np 16`が指定されている。

__UPDATE1.0__
First commit

__TODO__
何時間後に実行するか指定する
"""

# __BUILTIN MODULES__________________________
import glob
import subprocess as sp
from datetime import datetime
from tqdm import tqdm
import sys
import os
# __USER MODULES__________________________
from countdown import *

_command = ['runfeko', '-np', '16']


def command_gen(files: list) -> list:
    """
    実行コマンドのリストを返す

    引数:
        files: ファイルのリスト
    戻り値:
        li: コマンドのリスト
    """
    li = []
    for file in files:
        command = _command.copy()  # コマンドの初期化
        command.insert(1, file)  # コマンドにファイル名挿入
        li.append(command)  # コマンドをリストに格納
    return li


def confirm(files: list) -> str:
    """
    実行コマンドの確認

    引数:
        files: globで探されたファイル名(str型)
    戻り値:
        inp:y -> True / n -> False(bool型)
    """
    for command in command_gen(files):
        print(*command)  # 実行コマンドの確認
    dic = {'y': True, 'yes': True, 'n': False, 'no': False}
    while True:  # 正しい値が入力されるまで繰り返し
        try:
            inp = dic[input('以上のコマンドを実行します。よろしいですか？ y/n? >>>').lower()]
            break
        except:
            pass
        print('Error! Input again.')
    return inp


def excute(files: list, sleeptime: str):
    """
    runfekoの実行

    引数:
        _command:(リスト型)
        files:ファイル名(str型)
    戻り値:なし(commandの実行と、実行時間の表示)
    """
    count = 0

    if confirm(files):
        print('--\nyesが入力されました。処理を続行します。\n')
        if sleeptime:
            print('実行待ち...')
            try:
                countdown_end(sleeptime)  # sleeptimeの日時まで待つ
            except:
                countdown_shift(sleeptime)  # sleeptimeの時間だけ待つ
        for command in tqdm(command_gen(files)):
            count += 1
            print('実行サイクル: %d/%d' % (count, len(files)))

            ts = datetime.today()  # 開始時刻

            print('実行コマンド: ', *command)
            sp.call(command)  # コマンド実行

            te = datetime.today()  # 終了時刻

            print('開始時刻: ', ts)
            print('終了時刻: ', te)
            print('実行時間: ', te - ts)
    else:
        print('--\nNoが入力されました。\n処理終了します。')


if __name__ == '__main__':
    # files = glob.glob('../*.dat')  # TESTcommand
    try:
        regex = sys.argv[1]
    except:
        regex = input('正規表現でファイル名を入力してください。>>> ')

    try:
        sleeptime = sys.argv[2]
    except:
        sleeptime = input('何秒後に実行？ / 入力なし->Enterで直ちに実行 >>> ')

    dirname = os.path.dirname(regex)
    filename = os.path.basename(regex)
    if dirname:
        os.chdir(dirname)

    files = glob.glob1(dirname, filename)
    excute(files, sleeptime)
