# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: sendEmail.py
@Date ：2023/9/9 17:37
@Author：Amlei (lixiang.altr@qq.com)
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from glo import glo
from glo import log_info
from glo import log_error


class sendEmail():
    def __init__(self, receive):
        self.sender = ''  # 填写发信人的邮箱账号
        self.password = ''  # 发件人邮箱授权码
        self.receive = receive

    def email(self, text: str) -> None:
        send_text = f'{glo.today}实习{text}{glo.error}'
        try:
            match text:
                case "假期":
                    send_text = f'日期: {glo.today}为{text}，停止实习打卡!'
                case "周报":
                    send_text = f'{glo.today}{text}上传{glo.error}, 请检查本周{text}数据是否存在!'

            msg = MIMEText(send_text, 'plain', )  # 填写邮件内容
            msg['From'] = formataddr(("正方实习打卡", self.sender))  # 发件人邮箱昵称、账号
            msg['To'] = formataddr(("正方实习打卡", self.receive))  # 收件人邮箱昵称、账号
            msg['Subject'] = send_text  # 邮件标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件SMTP服务器
            server.login(self.sender, self.password)  # 发件人邮箱账号、授权码
            server.sendmail(self.sender, self.receive, msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、邮件信息
            server.quit()  # 关闭连接

            log_info(f"邮件已发送至{self.receive}")

        except Exception as error:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            log_error(f"邮件发送失败:{error}")


if __name__ == '__main__':
    email.email("周报")
