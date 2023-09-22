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
# from data import glo
from glo import glo
from glo import isWeekend
from log import Log
from sql import execute
from sql import SQL
from data import reportExecute
from sendEmail import mail

session = requests.session()

# Log("./").log()     # PATH


# 登录
def Login(option):
    global session

    # pprint.pprint(execute().data['user'][option])
    try:
        # 随即休眠5到11秒的浮点数
        sleep(float("{:.2f}".format(random.uniform(5, 11))))
        post = session.post(URL.loginURL, headers=URL.header, data=execute().data['user'][option])
        status(post, glo.login, option - 1)

        return post
    except requests.exceptions.SSLError:
        logging.error(f"{requests.exceptions.SSLError} SSL连接池异常")
        print(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Ubuntu后运行")
        exit()

# 打卡
def Sign(option):
    # global session
    """
    if check() == False:
        print("今日已打卡! 程序退出")
        exit()
    else:
        post = session.post(URL.signURL, data=state.datas)
        status(post, glo.sign)
    """
    # pprint.pprint(execute().data['state'][option])

    try:
        sleep(float("{:.2f}".format(random.uniform(2, 6))))

        post = session.post(URL.signURL, headers=session.headers, data=execute().data['state'][option])
        status(post, glo.sign, option-1)

        return post
    except requests.exceptions.SSLError:
        logging.error("SSL连接池异常")
        print("SSL连接池异常，请关闭代理或使用Ubuntu后运行")
        exit()

# 周报
def report(user: int):
    """
    开发阶段
    """
    data = reportExecute(user).data

    # print(data)

# 状态
def status(request, text, email):
    global session

    # if (request.status_code == 200 or (text == glo.sign and request.json()['status'] == "success")):
    if (request.status_code == 200):
        logging.info(f"{request.status_code} {text}{glo.success}")
        print(f"{request.status_code } {text}{glo.success}")
    else:
        logging.info(f"{text}{glo.error}, 请检查!")
        print(f"{text}{glo.error}, 请检查")
        try:
            mail(text, SQL().select(table='user')[email][-1])
        except:
            pass

if __name__ == '__main__':
    # print(SQL().count('user'))
    for i in range(1, SQL().count(table='user') + 1):
        Login(i)
        Sign(i)
        if (isWeekend(glo.Today) == True):
            report(123)
        # sleep(random.uniform(10, 20))
