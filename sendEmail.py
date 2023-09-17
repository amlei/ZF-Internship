# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: sendEmail.py
@Date ：2023/9/9 17:37
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from data import glo
from log import log

sender = '@qq.com'  # 填写发信人的邮箱账号
password = ''  # 发件人邮箱授权码

def mail(text,receive):
    try:
        msg = MIMEText(f'{glo.Today}实习{text}{glo.error}', 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["正方实习打卡", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["正方实习打卡", receive])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = f'{glo.Today}实习{text}{glo.error}'  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(sender, receive, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件已发送")

    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("邮件发送失败")

if __name__ == '__main__':
    mail("lixiang.thought@qq.com")