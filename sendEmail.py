# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: sendEmail.py
@Date ：2023/9/9 17:37
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from glo import glo
from chinese_calendar import is_holiday

class sendEmail():
    def __init__(self, receive):
        self.sender = ''  # 填写发信人的邮箱账号
        self.password = ''  # 发件人邮箱授权码
        self.receive = receive

    def email(self, text):
        send_text = f'{glo.Today}实习{text}{glo.error}'
        try:
            if text == "假期":
                send_text = f'日期: {glo.Today}为假期，停止实习打卡!'

            msg = MIMEText(send_text, 'plain', )  # 填写邮件内容
            msg['From'] = formataddr(["正方实习打卡", self.sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["正方实习打卡", self.receive])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = send_text  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
            server.login(self.sender, self.password)  # 括号中对应的是发件人邮箱账号、邮箱授权码
            server.sendmail(self.sender, self.receive, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            print("邮件已发送")
            logging.info("邮件已发送")

        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(f"邮件发送失败:{e}")
            logging.error(f"邮件发送失败:{e}")


if __name__ == '__main__':
    day = datetime.date(2023, 9, 27)

    assert is_holiday(day) is True