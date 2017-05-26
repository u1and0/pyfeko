"""Gmail送信"""
import smtplib
from email.mime.text import MIMEText
import datetime
import simplejson


def send_mail(mail_setting_file, send_file):
    """Send gmail
        to few address
        from designated address

    Usage: `send_mail(mail_setting_file='../ini/mail_setting.json', send_file='../ini/file.log')`

    # mail_setting_file: 送信先/元、パスワード設定
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
    # file.txt中に送信したい内容が入っている
    # with codecs.open('file.txt', 'r', 'utf-8') as f:
    with open(send_file) as f:
        raw_msg = f.read()
        jp = 'iso-2022-jp'
        msg = MIMEText(raw_msg.encode(jp), 'plain', jp)

    # MAIL SETTING
    with open(mail_setting_file, 'r') as jsonfile:
        param = simplejson.load(jsonfile)
    to_address = param['to_address']
    from_address = param['from_address']
    password = param['password']

    # Subject指定の時に使う
    date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    msg['Subject'] = date + " の使用情報"
    msg['From'] = from_address
    msg['To'] = ", ".join(to_address)

    # smtpサーバーへの接続
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(from_address, password)
    smtp.send_message(msg)
    smtp.close()
    return msg


if __name__ == '__main__':
    message = send_mail(mail_setting_file='../ini/mail_setting.json', send_file='../ini/file.log')
    print("Successfully sent email to {}\n".format(message['To']))
