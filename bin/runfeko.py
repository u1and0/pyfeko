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


def _select_files(filetypes, initialdir):
    filenames = filedialog.askopenfilenames(filetypes=filetypes, initialdir=initialdir)
    return filenames


class Runfeko:
    """docstring for Runfeko"""
    FILETYPES = [('テキストファイルとExcelファイル', '*.txt;*.csv')]
    ROOT = os.getcwd()
    COMMAND = ['runfeko', '-np', '16']  # runfekoの実行, -np 16: 16コアの使用

    def __init__(self):
        self.files = _select_files(self.FILETYPES, self.ROOT)
        self.commands = []
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
        command = Runfeko.COMMAND.copy()  # コマンドの初期化
        command.insert(1, file)  # コマンドにファイル名挿入
        return command

    def _execute(self, commands):
        send_mail = self.mailing_list.send('Runfekoテスト', command)
        return send_mail

    def _main(self):
        file_list = self._command_list_gen(self.files)
        execute_command = self._execute(file_list)
        return execute_command
