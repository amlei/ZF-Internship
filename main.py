# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: main.py
@Date ：2023/9/17 9:20
@Author：Amlei
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import pprint
from time import sleep
import requests
import logging
import random
from data import URL
from glo import glo
from glo import today_is_weekend
from log import Log
from sql import SQL
from data import reportExecute
from glo import today_is_holiday
from data import userExecute
from sendEmail import sendEmail

Log("./").log()     # PATH

class app():
    def __init__(self):
        self.session = requests.session()
        self.header = URL.header
        self.user = None
        self.email = None

    def update_data(self, username: int, mail: str) -> None:
        self.user = username
        self.email = mail

    # 登录打卡
    def launch(self, table: str):
        url = None
        status = None   # 当前执行状态
        data = None
        if table == 'user':  # 登录
            url = URL.loginURL
            status = glo.login
            data = 'user'
        elif table == 'state':  # 打卡
            url = URL.signURL
            status = glo.sign
            data = 'state'
        else:
            exit()

        try:
            # 随即休眠30到60秒的浮点数
            # sleep(float("{:.2f}".format(random.uniform(30, 45))))
            sleep(float("{:.2f}".format(random.uniform(5, 10))))
            post = self.session.post(url, headers=self.header, data=userExecute(self.user).data[data])

            # 将原有的header覆盖，防止无法成功执行后续操作
            self.header = post.request.headers
            self.status(post, status)

            return post
        except requests.exceptions.SSLError:
            logging.error(f"{requests.exceptions.SSLError} SSL连接池异常")
            print(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Ubuntu后运行")
            exit()

    # 周报
    def report(self):
        # 随即休眠六至十分钟
        # dormancy = float("{:.2f}".format(random.uniform(360, 600)))
        dormancy = float("{:.2f}".format(random.uniform(10, 15)))
        print(f"休眠{dormancy}秒")
        sleep(dormancy)
        # 上传周报数据
        if reportExecute(self.user).data is None:
            pass
        else:
            post = self.session.post(URL.reportURL, headers=self.header, data=reportExecute(self.user).data)
            self.status(post, glo.report)

            return post

    # 状态
    def status(self, request, text: str) -> None:
        if request.status_code == 200:
            logging.info(f"{request.status_code} {text}{glo.success}")
            print(f"{request.status_code} {text}{glo.success}")

            # 如果当前打卡执行完毕, 且今日为星期六则上传周报
            # 再重刷新header, 以供下一个用户能够正常执行打卡
            if text == glo.sign and today_is_weekend():
                self.report()
                self.refresh_header()

        # 应以网站打卡操作为优先，而非先判断是否为假期
        elif request.status_code != 200 and date_is_holiday(glo.Today) is True:
            print("今日是假期，停止打卡")
            logging.info("今日是假期，停止打卡")
            # 发送邮箱
            user = SQL().allUser()
            for j in range(0, len(user)):
                sendEmail(user[j][1]).email("假期")
            # sendEmail(self.user).email("假期")

            # 执行完退出
            exit()
        else:
            logging.info(f"{text}{glo.error}, 请检查!")
            print(f"{text}{glo.error}, 请检查")
            sendEmail(self.email).email(text)
            # 执行完退出
            exit()

    def refresh_header(self) -> None:
        self.header = URL.header

def main() -> None:
    user = SQL().allUser()
    appLaunch = app()

    for i in range(0, len(user)):
        yhm = user[i][0]
        email = user[i][1]
        # 加载用户名、密码
        appLaunch.update_data(yhm, email)

        # 登录
        appLaunch.launch('user')
        # 打卡
        appLaunch.launch('state')

if __name__ == '__main__':
    main()