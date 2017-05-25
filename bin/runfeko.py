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
import smtplib
from email.mime.text import MIMEText
import datetime
import codecs
import simplejson


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
        print(commands)

    def _mail(self, logfile):
        """Send mail to many address
        from designated address
        """
        # file.txt中に送信したい内容が入っている
        # with codecs.open('file.txt', 'r', 'utf-8') as f:
        with open(logfile) as f:
            raw_msg = f.read()
            jp = 'iso-2022-jp'
            msg = MIMEText(raw_msg.encode(jp), 'plain', jp)

        # MAIL SETTING
        with open('./ini/mail_setting.json', 'r') as jsonfile:
            param = simplejson.load(jsonfile)
        to_address = param['to_address']
        from_address = param['from_address']
        password = param['password']

        # Subject指定の時に使う
        date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        msg['Subject'] = date + " の使用情報"
        msg['From'] = from_address
        # smtpサーバーへの接続
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_address, password)
        for to_add in to_address:
            msg['To'] = to_add
            print(msg)
            smtp.send_message(msg)
            print("Successfully sent email to {}\n".format(to_add))
            msg['To'] = None
        else:
            smtp.close()

    def _main(self):
        coml = self._command_list_gen(self.files)
        self._execute(coml)
        self.mail()
