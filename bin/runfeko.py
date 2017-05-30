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


def _execute(command_dic):
    """command_dicの実行
    引数command_dic(ディクショナリ形式)の実行
    command: `['runfeko', <filename>, '-np', '16']`
    cwd: 選択したファイル名のディレクトリ
    """
    # command_dic.insert(0, sys.executable)  # 'C:\\tools\\Anaconda3\\python.exe'がコマンドリストに追加される
    print('\n===Execute===\n{}\n\n'.formant(command_dic['command']))
    run = sp.call(command_dic['command'],
                  creationflags=sp.CREATE_NEW_CONSOLE, cwd=command_dic['cwd'])
    return run


class Runfeko:
    """FEKO実行のスケジューラ
    1. preファイルの選択
    2. 実行
    3. メールの送信(logファイル、エラー出力)
    """
    FILETYPES = [('PREFEKO files', '*.pre;*.fek')]
    ROOT = os.getcwd()
    COMMAND = ['runfeko', '-np', '16']  # runfekoの実行, -np 16: 16コアの使用

    def __init__(self, mail_setting='./ini/mail_setting.json'):
        self.files = self._select_files(self.FILETYPES, self.ROOT)
        self.commands = self._command_list_gen(self.files)
        self.mailing_list = Gmail(mail_setting)

    def _select_files(self, filetypes, initialdir):
        """ファイルの選択"""
        filenames = filedialog.askopenfilenames(filetypes=filetypes, initialdir=initialdir)
        return filenames

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
        command.insert(1, os.path.basename(file))  # コマンドにファイル名挿入
        command_dic = {'command': command, 'cwd': os.path.dirname(file)}
        return command_dic

    def _main(self):
        body = self.commands
        self.mailing_list.send('Runfekoテスト', str(body))
        for command in body:
            result = _execute(command)
            self.mailing_list.send('Runfekoテスト', result)
        return body


if __name__ == '__main__':
    task = Runfeko()
    task._main()
