# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: log.py
@Date ：2023/9/4 16:23
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
# from data import glo
import glo
import os
import logging

class Log:
    def __init__(self, path):
        self.path = path

    # 判断系统日志目录是否存在，否则创建
    def isExistsDir(self, dir):
        if (os.path.exists(f'{self.path}{dir}')):
            print("Dir pass")
            pass
        else:
            os.mkdir(f"{self.path}{dir}")

        return True

    # 日志记录
    def log(self):
        self.isExistsDir("log")

        # logging.basicConfig(filename=f'./log/{glo.Today.strftime("%Y-%m-%d")}.log', format='%(levelname)s :%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

        # Aliyun Server
        logging.basicConfig(filename=f'{self.path}log/{glo.Today}.log', format='%(levelname)s :%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

    # 成功打卡次数 -----> 待实现
    def useNumber(self):
        self.isExistsDir("usage-rate")
        try:
            file = open("usage-rate/number.txt")
            print(file.read())
        except FileNotFoundError:
            file = open("usage-rate/number.txt", "w")
            if self.check() == False:
                file.write("1")
                file.close()

    # 检查今日是否打卡 ----> 待实现
    def check(self):

        if (self.isExistsDir( "log")):
            file = open(f"./log/{glo.Today}.txt", "r", encoding="utf-8").readlines()
            # 以防今日未打卡, 日志为空白情况出现异常
            try:
                if file[-2].split(" ")[-1][2:4] == glo.success:
                    logging.warning("今日已打卡")
                    return False  # False -> 已打卡 True -> 未打卡
            except:
                logging.info("今日未打卡 ")
                return True


if __name__ == '__main__':
    PATH = "./"
    Log(PATH).log()
    logging.basicConfig(filename=f'./log/{glo.Today.strftime("%Y-%m-%d")}.log', format="%(levelname)s :%(asctime)s %(message)s", encoding='utf-8', level=logging.DEBUG)
    logging.basicConfig(filename=f'/home/ya/code/python/ZF-Internship/HTTP/log/{glo.Today}.log', format="%(levelname)s :%(asctime)s %(message)s", encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like resund and Malmö')

    # PATH = "./"


    print(" ")
