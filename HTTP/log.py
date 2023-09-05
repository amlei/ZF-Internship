# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: log.py
@Date ：2023/9/4 16:23
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
import time
from data import glo
import os
import logging

Time = time.localtime()
Today = f"{Time.tm_year}-{Time.tm_mon}-{Time.tm_mday}"

# 判断系统日志目录是否存在，否则创建
def isExistsDir(dir):
    if (os.path.exists(f'./{dir}')):
        print("pass")
        pass
    else:
        os.mkdir(f"./{dir}")

# 日志记录
def log():
    global Today
    isExistsDir("log")

    logging.basicConfig(filename=f'./log/{Today}.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

# 成功打卡次数 -----> 待实现
def useNumber():
    isExistsDir("use")
    try:
        file = open("./use/number.txt")
        print(file.read())
    except FileNotFoundError:
        file = open("./use/number.txt", "w")
        if check() == False:
            file.write("1")
            file.close()

# 检查今日是否打卡 ----> 待实现
def check():
    global Today

    if (isExistsDir("log")):
        file = open(f"./log/{Today}.txt", "r", encoding="utf-8").readlines()
        # 以防今日未打卡, 日志为空白情况出现异常
        try:
            if file[-2].split(" ")[-1][2:4] == glo.success:
                logging.warning("今日已打卡")
                return False  # False -> 已打卡 True -> 未打卡
        except:
            logging.info("今日未打卡 ")
            return True


if __name__ == '__main__':
    # logging.basicConfig(filename='./log/example1.log', encoding='utf-8', level=logging.DEBUG)
    # # logging.debug('This message should go to the log file')
    # # logging.info('So should this')
    # # logging.warning('And this, too')
    # # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
    # logging.warning('is when this event was logged.')
    # logging.warning('is when this event was logged.')
    # log()
    # logging.info("Hello Test")
    # print(tempfile.mkdtemp(suffix="T", prefix="H", dir="./"))

    # os.mkdir("./TestDir")
    # log()
    print(" ")
