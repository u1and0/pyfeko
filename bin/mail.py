"""Gmail送信"""
import smtplib
from email.mime.text import MIMEText
import simplejson
import os


class Gmail:
    """Send gmail
    複数の宛先にgmailを送信する。
    送信先/元、パスワードはJSON形式で記述し、 引数にファイルパスを入れる。

    Usage:
        hoge = gmail('./ini/mail.setting')
        hoge.send('タイトル', '本文か本文が入ったファイルパス')
    """

    HOST, PORT = "smtp.gmail.com", 587

    def __init__(self, setting_file):
        """
        `setting_file` はJSON形式で記述
        送信先、送信元、パスワードを以下のように記述

        ```JSON:setting_file
            {
                "to_address": ["example1@gmail.com", "example2@hotmail.co.jp"],
                "from_address": "source@gmail.com",
                "password": "12345678"
            }
        ```

        送信元アドレスは以下の操作が必要
            * 2段階プロセス->オフ
            * 安全性の低いアプリのアクセス->許可
            > 参考: http://qiita.com/HirofumiYashima/items/1b24397c2e915658c984

        """
        with open(setting_file, 'r') as jsonfile:  # 宛先、差出人、差出人パスワード
            param = simplejson.load(jsonfile)
        self.to_address = param['to_address']
        self.from_address = param['from_address']
        self.password = param['password']

    def _write(self, subject, body):
        """Set mail subject from, to"""
        if os.path.isfile(body):  # bodyがファイルとして渡された場合
            with open(body, 'r') as f:  # メールの本文
                raw_msg = f.read()
        else:  # bodyがファイルでない場合
            raw_msg = body
        jp = 'iso-2022-jp'
        message = MIMEText(raw_msg.encode(jp), 'plain', jp)
        message['Subject'] = subject
        message['From'] = self.from_address
        message['To'] = ", ".join(self.to_address)
        return message

    def send(self, subject, body):
        """Connect smtp server
        Usage:
            gmail.send('title', 'some messege or file path')
        """
        smtp = smtplib.SMTP(self.HOST, self.PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.from_address, self.password)
        mail_message = self._write(subject, body)
        smtp.send_message(mail_message)
        smtp.close()
        return mail_message
