#!/bin/env python3
"""FEKOの逐次実行スケジューラ
# USAGE
## @Windows env
* Click `runfeko.bat`
* Select files

## @Linux env
```
$ cd
$ ,/runfeko
```

# FUNCTION
"""
from tkinter import filedialog
import os


def _select_files(filetypes, initialdir):
    filenames = filedialog.askopenfilenames(filetypes=filetypes, initialdir=initialdir)
    return filenames


class Runfeko:
    """docstring for Runfeko"""
    FILETYPES = [('テキストファイルとExcelファイル', '*.txt;*.csv')]
    ROOT = os.getcwd()
    COMMAND = ['runfeko', '-np', '16']  # runfekoの実行, -np 16: 16コアの使用

    def __init__(self):
        self.files = _select_files(Runfeko.FILETYPES, Runfeko.ROOT)
        self.commands = []

    def _main(self):
        for file in self.files:
            next_command = self._generate(file)
            self.commands.append(next_command)  # コマンドをリストに格納
        self._execute()
        self._mail()

    def _generate(self, file):
        """実行コマンドのリストを返す
        args: files: ファイルのリスト
        return: li: コマンドのリスト
        """
        command = Runfeko.COMMAND.copy()  # コマンドの初期化
        command.insert(1, file)  # コマンドにファイル名挿入
        return command

    def _execute(self):
        pass

    def _mail(self):
        pass
