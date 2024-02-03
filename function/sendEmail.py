# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: sendEmail.py
@Date ：2023/9/9 17:37
@Author：Amlei (lixiang.altr@qq.com)
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import function.data
from function.glo import Glo
from function.glo import log_info
from function.glo import log_error


class SendEmail:
    def __init__(self, receive: str):
        self.sender: str = '@qq.com'  # 填写发信人的邮箱账号
        self.password: str = ''       # 发件人邮箱授权码
        self.receive: str = receive
        self.classify = None

    def title(self) -> str:
        """ 邮箱标题 """
        send_title: str = f'{Glo.today}实习{self.classify}{Glo.error}'
        match self.classify:
            case Glo.festival:
                send_title = f'日期: {Glo.today}为{self.classify}，停止实习打卡!'
            case Glo.report:
                send_title = f'{Glo.today}{self.classify}上传{Glo.error}, 请检查本周{self.classify}数据是否存在!'
            case Glo.log:
                send_title = f'{Glo.today}实习打卡{self.classify}'

        return send_title

    def email(self) -> str:
        """ 邮箱信息初始化 """
        msg = MIMEText(function.data.send_log, 'plain')  # 填写邮件内容
        msg['From'] = formataddr(("正方实习打卡", self.sender))  # 发件人邮箱昵称、账号
        msg['To'] = formataddr(("正方实习打卡", self.receive))  # 收件人邮箱昵称、账号
        msg['Subject'] = self.title()  # 邮件标题

        return msg.as_string()

    def send(self, classify: str) -> None:
        """ 邮箱发送 """
        try:
            self.classify = classify
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件SMTP服务器
            server.login(self.sender, self.password)  # 发件人邮箱账号、授权码
            server.sendmail(self.sender, self.receive, self.email())  # 发件人邮箱账号、收件人邮箱账号、邮件信息
            server.quit()  # 关闭连接

            log_info(f"邮件已发送至{self.receive}")
        except Exception as error:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            log_error(f"邮件发送失败:{error}")

    def log(self) -> None:
        """ 日志发送 —— 文本形式 """
        self.send(Glo.log)

if __name__ == '__main__':
    se = SendEmail("@qq.com")
    se.send("周报")