#!/bin/env python
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
from mail import Gmail
import subprocess as sp
import sys


def _select_files(filetypes, initialdir):
    filenames = filedialog.askopenfilenames(filetypes=filetypes, initialdir=initialdir)
    return filenames


class Runfeko:
    """FEKO実行のスケジューラ
    1. preファイルの選択
    2. 実行
    3. メールの送信(logファイル、エラー出力)
    """
    FILETYPES = [('テキストファイルとExcelファイル', '*.txt;*.csv')]
    # FILETYPES = [('PREFEKO files', '*.pre;*.inc')]
    ROOT = os.getcwd()
    COMMAND = ['runfeko', '-np', '16']  # runfekoの実行, -np 16: 16コアの使用

    def __init__(self):
        self.files = _select_files(self.FILETYPES, self.ROOT)
        self.commands = self._command_list_gen(self.files)
        self.mailing_list = Gmail('./ini/mail_setting.json')

    def _command_list_gen(self, files):
        """実行コマンド生成(self._generate())をすべてのファイルに適用したlist(words) of list(tasks)を返す"""
        command_list = map(self._generate, files)
        return list(command_list)

    def _generate(self, file):
        """実行コマンドを返す
        args:  filename
        return: one command
        """
        command = self.COMMAND.copy()  # コマンドの初期化
        command.insert(1, file)  # コマンドにファイル名挿入
        return command

    def _execute(self, commands):
        run = sp.Popen(commands, creationflags=sp.CREATE_NEW_CONSOLE)
        return run

    def _main(self):
        command=self.commands
        # result = self._execute(command[0])
        send_mail = self.mailing_list.send('Runfekoテスト', str(command))
        return send_mail
