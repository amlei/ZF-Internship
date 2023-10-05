# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: main.py
@Date ：2023/9/17 9:20
@Author：Amlei
@version：python 3.11
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

    def update_data(self, username: int, mail: str):
        self.user = username
        self.email = mail

    # 登录打卡
    def launch(self, table: str):
        url = None
        status = None  # 当前执行状态
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
            sleep(float("{:.2f}".format(random.uniform(30, 45))))
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
        """
        开发阶段
        """
        # 随即休眠六至十分钟
        dormancy = float("{:.2f}".format(random.uniform(360, 600)))
        print(f"休眠{dormancy}秒")
        sleep(dormancy)

        post = self.session.post(URL.reportURL, headers=self.header, data=reportExecute(self.user).data)

        logging.info(post.status_code)
        logging.info(post.text)

        print(post.status_code)
        print("响应信息：", post.text)
        self.status(post, "周报")

        return post

    # 状态
    def status(self, request, text: str):
        # if (request.status_code == 200 or (text == glo.sign and request.json()['status'] == "success")):
        if request.status_code == 200:
            logging.info(f"{request.status_code} {text}{glo.success}")
            print(f"{request.status_code} {text}{glo.success}")
            # 每个账户完成打卡后，重刷新header
            if text == glo.sign:
                self.refresh_header()
        # 应以网站打卡操作为优先，而非先判断是否为假期
        elif request.status_code != 200 and date_is_holiday(glo.Today) is True:
            print("今日是假期，停止打卡")
            logging.info("今日是假期，停止打卡")
            # 发送邮箱
            for j in range(0, len(user)):
                sendEmail(user[j][1]).email("假期")
            # 执行完退出
            exit()
        else:
            logging.info(f"{text}{glo.error}, 请检查!")
            print(f"{text}{glo.error}, 请检查")
            sendEmail(self.email).email(text)
            # 执行完退出
            exit()

    def refresh_header(self):
        self.header = URL.header

if __name__ == '__main__':
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

        # 若当前为星期六，则上传周报 ----> 周报数据已存在MySQL数据库中
        # if (today_is_weekend() == False):
        #     app(yhm, email).report()
        #     pprint.pprint(reportExecute(yhm).data)