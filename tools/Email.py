__author__ = "无声"

# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib,os,inspect
from email.mime.text import MIMEText
from email.header import Header
from DreamMultiDevices.tools import Config

def sendemail(message):
    # 第三方 SMTP 服务
    configPath=os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())) + os.path.sep + ".")) + os.path.sep + ".")+"\config.ini"
    mail_host= Config.getEmail(configPath, "mail_host")
    mail_user= Config.getEmail(configPath, "mail_user")
    mail_pass= Config.getEmail(configPath, "mail_pass")
    sender = Config.getEmail(configPath, "sender")
    receivers =  Config.getEmail(configPath, "receivers")
    print(mail_host,mail_user,mail_pass,sender,receivers)
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")

