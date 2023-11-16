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
import logging
from function.data import URL
from function.glo import glo
from function.glo import self_sleep
from function.glo import today_is_weekend
from function.log import Log
from function.sql import SQL
from function.data import reportExecute
from function.glo import date_is_holiday
from function.glo import log_info
from function.glo import log_error
from function.data import userExecute
from function.sendEmail import sendEmail
from bs4 import BeautifulSoup

Log("./").log()   # Path

class app():
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
            self.status(post, glo.login)

            return post
        except requests.exceptions.SSLError:
            log_error(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Linux后运行")
            exit()
        
    # 打卡
    def sign(self) -> requests:
        # 若已打卡则跳过
        if self.isSign():
            log_info(f"{self.user} {glo.today} 已打卡")
            pass
        else:
            try:
                post = self.session.post(URL.signURL, headers=self.header, data=userExecute(self.user).data['state'])
                self.header = post.request.headers
                self.status(post, glo.login)

                return post
            except requests.exceptions.SSLError:
                log_error(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Linux后运行")
                exit()

    # 周报
    def report(self) -> requests:
        # 随即休眠1至3分钟
        self_sleep(10, 29, f"{self.user}上传周报")
        
        # 上传周报数据
        if len(reportExecute(self.user).data) == glo.null:
            sendEmail(self.email).email(text=glo.report)
            pass
        else:
            post = self.session.post(URL.reportURL, headers=self.header, data=reportExecute(self.user).data)
            self.status(post, glo.report)

            return post

    # 执行状态
    def status(self, request, text: str) -> None:

        if request.status_code == 200:
            if text == glo.login and BeautifulSoup(request.text, 'html.parser').find('div', class_='username hidden-xs'):
                log_info(f"{self.user} {request.status_code} {text}{glo.success}")

            elif text == glo.sign and json.loads(request.text)['status'] == 'success':
                log_info(f"{self.user} {request.status_code} {text}{glo.success}")

                match today_is_weekend():
                    # 如果当前打卡执行完毕, 且今日为星期六则上传周报
                    case True:
                        self.report()
                    # # 非上传周报情况，直接刷新header
                    # case False:
                    #     self.refresh_header()
                    #     self.refresh_session()
            # 周报上传成功后会再次进入status函数，从而执行到本行判断是否上传成功条件，
            # 若上传成功则刷新header 以供下一个用户能够正常执行打卡
            elif text == glo.report and json.loads(request.text)['status'] == 'success':
                log_info(f"{self.user} {request.status_code} {text}{glo.success}")
                # self.refresh_header()
                # self.refresh_session()

        # 应以网站打卡操作为优先，而非先判断是否为假期
        elif request.status_code != 200 and date_is_holiday(glo.today) is True:
            print("今日是假期，停止打卡")
            logging.info("今日是假期，停止打卡")
            # 发送邮箱
            user = userData()
            while user:
                sendEmail(user.pop()[1]).email(glo.festival)
            # 执行完退出
            exit()
        else:
            log_info(f"{self.user} {text}{glo.error}, 请检查!")
            sendEmail(self.email).email(text)
            # 当前账户无本周周报，仅跳过该账户
            # 若为登录或打卡失败则直接退出程序
            if text == glo.report:
                # self.refresh_header()
                # self.refresh_session()
                pass
            else:
                exit()

    def refresh_header(self) -> None:
        self.header = URL.header

    def refresh_session(self) -> None:
        print("开启新Session")
        self.session = requests.session()

    # 打卡状态
    def isSign(self) -> bool:
        # 查看打卡状态
        self_sleep(10, 20)
        sign_post_status = self.session.post(URL.singInfoUrl, headers=self.header)

        # 已打卡为 True, 否则为 False
        return len(json.loads(sign_post_status.text)) != 0

# 提供检索用户
def userData() -> list:
    return list(SQL().allUser())

def main() -> None:
    user = userData()

    while user:
        appLaunch = app()
        pop_user = user.pop(0)
        yhm = pop_user[0]
        email = pop_user[1]
        print(yhm, email)

        # 加载用户名、密码
        appLaunch.update_data(yhm, email)
        # 登录
        appLaunch.login()
        # 打卡
        appLaunch.sign()

        # 每个用户打卡完成后休眠
        self_sleep(60, 120, f"{yhm} 打卡完成，开始下个用户")


if __name__ == '__main__':
    main()
