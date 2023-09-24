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
from glo import isWeekend
from log import Log
from sql import SQL
from data import reportExecute
from data import userExecute
from sendEmail import mail

Log("./").log()     # PATH

class app():
    def __init__(self, user, email):
        self.session = requests.session()
        self.user = user
        self.email = email

    # 登录打卡
    def launch(self, table: str):
        url = None
        gloD = None
        data = None
        if table == 'user':     # 登录
            url = URL.loginURL
            gloD = glo.login
            data = 'user'
        elif table == 'state':     # 打卡
            url = URL.signURL
            gloD = glo.sign
            data = 'state'
        else:
            exit()

        try:
            # 随即休眠3到60秒的浮点数
            sleep(float("{:.2f}".format(random.uniform(30, 60))))
            post = self.session.post(url, headers=URL.header, data=userExecute(self.user).data[data])

            self.status(post, gloD)

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
        sleep(float("{:.2f}".format(random.uniform(360, 600))))
        post = self.session.post(URL.reportURL, headers=self.session.headers, data=reportExecute(self.user).data)

        self.status(post, "周报")

    # 状态
    def status(self, request, text: str):
        # if (request.status_code == 200 or (text == glo.sign and request.json()['status'] == "success")):
        if (request.status_code == 200):
            logging.info(f"{request.status_code} {text}{glo.success}")
            print(f"{request.status_code} {text}{glo.success}")
        else:
            logging.info(f"{text}{glo.error}, 请检查!")
            print(f"{text}{glo.error}, 请检查")
            try:
                mail(text, self.email)
            except:
                pass

if __name__ == '__main__':
    # print(SQL().count('user'))
    user = SQL().allUser()

    for i in range(0, len(user)):
        yhm = user[i][0]
        email = user[i][1]
        # 登录
        app(yhm, email).launch('user')
        # 打卡
        app(yhm, email).launch('state')
        # 若当前为星期六，则上传周报 ----> 周报数据已存在MySQL数据库中
        if (isWeekend(glo.Today) == True):
            app(yhm, email).report()

