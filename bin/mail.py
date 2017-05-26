"""Gmail送信"""
import smtplib
from email.mime.text import MIMEText
import simplejson
import codecs


def send_mail(setting, subject, body):
    """Send gmail
        to few address
        from designated address

    Usage: `send_mail(setting='../ini/mail_setting.json', body='../ini/file.log')`

    # setting: 送信先/元、パスワード設定
    '../ini/mail_setting.json': JSON形式で記述

        * 送信先アドレス(例:"to_address": ["foo@gmail.com", "bar@hotmail.co.jp"])
        * 送信元アドレス(例: "from_address": "foobar@gmail.com")
        * 送信元アドレスのパスワード(例: "password": "12345678")

    ## 送信先アドレスはリスト形式で複数記述可能
    参考: https://stackoverflow.com/questions/8856117/how-to-send-email-to-multiple-recipients-using-python-smtplib

    ## 送信元アドレスは以下の操作が必要

    * 2段階プロセス->オフ
    * 安全性の低いアプリのアクセス->許可

    参考: http://qiita.com/HirofumiYashima/items/1b24397c2e915658c984
    """

    # ---------Get mail setting----------
    with open(setting, 'r') as jsonfile:  # 宛先、差出人、差出人パスワード
        param = simplejson.load(jsonfile)
    to_address = param['to_address']
    from_address = param['from_address']
    password = param['password']

    # ---------Set mail body, subject from, to----------
    with codecs.open(body, 'r', 'utf-8') as f:
        # with open(body, 'r') as f:  # メールの本文
        raw_msg = f.read()
    jp = 'iso-2022-jp'
    message = MIMEText(raw_msg.encode(jp), 'plain', jp)
    message['Subject'] = subject
    message['From'] = from_address
    message['To'] = ", ".join(to_address)

    # ---------Connect smtp server----------
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(from_address, password)
    smtp.send_message(message)
    smtp.close()

    return message
