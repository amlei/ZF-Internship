# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: main.py
@Date ：2023/9/4 16:16
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
from time import sleep

import requests
import logging
import random
from data import URL
from data import user
from data import state
from data import glo
from log import log
from log import check

session = requests.session()

random.seed(1.36)

log()

# 登录
def Login():
    global session

    try:
        post = session.post(URL.loginURL, data=user.user)
        if post.status_code == 403:
            # 随即休眠5到11秒的浮点数
            sleep(float("{:.2f}".format(random.uniform(5, 11))))
            post = session.post(URL.loginURL, headers=URL.header, data=user.user)
        status(post, glo.login)

        return post
    except requests.exceptions.SSLError:
        logging.error(f"{requests.exceptions.SSLError} SSL连接池异常")
        print(f"{requests.exceptions.SSLError} SSL连接池异常，请关闭代理或使用Ubuntu后运行")
        exit()


# 打卡
def Sign():
    global session
    """
    if check() == False:
        print("今日已打卡! 程序退出")
        exit()
    else:
        post = session.post(URL.signURL, data=state.datas)
        status(post, glo.sign)
    """

    try:
        sleep(float("{:.2f}".format(random.uniform(2, 6))))

        post = session.post(URL.signURL, headers=session.headers, data=state.datas)
        status(post, glo.sign)

        return post
    except requests.exceptions.SSLError:
        logging.error("SSL连接池异常")
        print("SSL连接池异常，请关闭代理或使用Ubuntu后运行")
        exit()

# 状态
def status(request, text):
    global session

    # if (request.status_code == 200 or (text == glo.sign and request.json()['status'] == "success")):
    if (request.status_code == 200):
        logging.info(f"{request.status_code} {text}{glo.success}")
        print(f"{request.status_code } {text}{glo.success}")
    else:
        logging.info(f"{text}{glo.error}, 请检查!")
        print(f"{text}{glo.error}, 请检查")

if __name__ == '__main__':
    Login()
    Sign()
