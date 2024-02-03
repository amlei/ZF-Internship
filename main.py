# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: main.py
@Date ：2023/9/17 9:20
@Author：Amlei (lixiang.altr@qq.com)
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import json
import requests
from function.data import URL
from function.data import reportExecute
from function.data import userExecute
from function.glo import Glo
from function.glo import self_sleep
from function.glo import today_is_weekend
from function.glo import date_is_holiday
from function.glo import log_info
from function.glo import log_error
from function.glo import random_time
from function.log import Log
from function.sql import SQL
from function.sendEmail import SendEmail
from bs4 import BeautifulSoup
from datetime import datetime

Log("./").log()   # Path


class App:
    def __init__(self):
        self.session = requests.session()
        self.header = URL.header
        self.user = None
        self.email = None

    # 载入用户数据
    def update_data(self, username: int, mail: str) -> None:
        self.user = username
        self.email = mail

    # 登录
    def login(self) -> requests:
        try:
            post = self.session.post(URL.loginURL, headers=self.header, data=userExecute(self.user).data['user'])
            # 将原有的header覆盖，防止无法成功执行后续操作
            self.header = post.request.headers
            self.status(post, Glo.login)

            return post
        except requests.exceptions.SSLError:
            log_error(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Linux后运行")
            exit()

    # 打卡
    def sign(self) -> requests:
        # 若已打卡则跳过
        if self.isSign():
            log_info(f"{self.user} {Glo.today} 已打卡")
            pass
        else:
            try:
                post = self.session.post(URL.signURL, headers=self.header, data=userExecute(self.user).data['state'])
                self.header = post.request.headers
                self.status(post, Glo.sign)

                return post
            except requests.exceptions.SSLError:
                log_error(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Linux后运行")
                exit()

    # 签退
    def sing_out(self) -> requests:
        # 若当前时间为 18 点后且未签退
        if self.isSign():
            try:
                # log_info(f"{self.user} 签退")
                print(f"{self.user} 签退")
                # 更改签退信息
                userdata = userExecute(self.user).data['state']
                userdata['kqlx'] = 1

                post = self.session.post(URL.signURL, headers=self.header, data=userdata)
                self.header = post.request.headers
                self.status(post, Glo.sing_out)

                return post
            except requests.exceptions.SSLError:
                log_error(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Linux后运行")
                exit()

    # 周报
    def report(self) -> requests:
        # 随即休眠1至3分钟
        self_sleep(10, 29, f"{self.user}上传周报")

        # 上传周报数据
        if len(reportExecute(self.user).data) == Glo.null:
            SendEmail(self.email).send(Glo.report)

            pass
        else:
            post = self.session.post(URL.reportURL, headers=self.header, data=reportExecute(self.user).data)
            self.status(post, Glo.report)

            return post

    # 执行状态
    def status(self, request, text: str) -> None:
        if request.status_code == 200:
            if text == Glo.login and BeautifulSoup(request.text, 'html.parser').find('div', class_='username hidden-xs'):
                log_info(f"{self.user} {request.status_code} {text}{Glo.success}")

            elif text == Glo.sign and json.loads(request.text)['status'] == 'success':
                log_info(f"{self.user} {request.status_code} {text}{Glo.success}")

                match today_is_weekend():
                    # 如果当前打卡执行完毕, 且今日为星期六则上传周报
                    case True:
                        self.report()

            # 周报上传成功后会再次进入status函数，从而执行到本行判断是否上传成功条件，
            elif (text == Glo.report or text == Glo.sing_out) and json.loads(request.text)['status'] == 'success':
                log_info(f"{self.user} {request.status_code} {text}{Glo.success}")

        # 应以网站打卡操作为优先，而非先判断是否为假期
        elif request.status_code != 200 and date_is_holiday(Glo.today) is True:
            log_info("今日是假期，停止打卡")
            # 发送邮箱
            user = userData()
            while user:
                SendEmail(user.pop()[1]).send(Glo.festival)
            # 执行完退出
            exit()
        else:
            log_info(f"{self.user} {text}{Glo.error}, 请检查!")
            SendEmail(self.email).send(text)
            # 当前账户无本周周报，仅跳过该账户
            # 若为登录或打卡失败则直接退出程序
            if text == Glo.report:
                pass
            else:
                exit()

    # 打卡状态
    def isSign(self) -> bool:
        # 查看打卡状态
        self_sleep(10, 20)
        sign_post_status = self.session.post(URL.singInfoUrl, headers=self.header)

        # 已打卡为 True, 否则为 False
        return len(json.loads(sign_post_status.text)) != Glo.null


def userData() -> list:
    """
    提供检索用户
    """
    return list(SQL().allUser())


def main() -> None:
    user = userData()
    # length: int = len(user)
    # 第一个打卡用户同样需要休眠
    rt: list[int] = random_time()

    self_sleep(rt.pop(0), rt.pop(0))

    i: int = 0
    # 指定之后的用户需要付费后才能打卡
    while user:
        launch = App()
        pop_user = user.pop()
        yhm = pop_user[0]
        email = pop_user[1]

        # 加载用户名、密码
        launch.update_data(yhm, email)
        # 登录
        launch.login()

        # 调用函数前判断当前是否为打卡时间段
        if datetime.now().hour < Glo.sing_out_time:
            # 打卡
            launch.sign()
        else:
            # 签退
            launch.sing_out()

        i += 1
        if i >= 3:
            break
        # 每个用户打卡完成后休眠
        rt = random_time()
        self_sleep(rt.pop(0), rt.pop(0), f"{yhm} 打卡完成，开始下个用户")

    # 执行完全部用户打卡，日志发送给代码所有者
    SendEmail("@qq.com").log()

if __name__ == '__main__':
    main()
