#!/bin/env python3
"""Test of pyfeko/bin/mail.py"""
import sys
sys.path.append('./bin')
import mail

message = mail.send_mail(setting='./ini/mail_setting.json',
                    subject='テスト　runfeko', body='./ini/file.log')
print("Successfully sent email to {}\n".format(message['To']))
