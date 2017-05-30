#!/bin/env python
"""Test of pyfeko/bin/mail.py"""
import sys
sys.path.append('./bin')
import mail

# message = mail.send_mail(setting='./ini/mail_setting.json',
#                     subject='テスト　runfeko', body='./ini/file.log')
# print("Successfully sent email to {}\n".format(message['To']))

alert = mail.Gmail(setting_file='./ini/mail_setting.json')
alert.send(subject='テスト　runfeko', body='./ini/file.log')
alert.send('テスト　runfeko', '本文は\nここにテキスト書いても良い')