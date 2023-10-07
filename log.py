# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: log.py
@Date ：2023/9/4 16:23
@Author：Amlei
@version：python 3.12
@IDE: PyCharm 2023.2
"""
from glo import glo
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

        logging.basicConfig(filename=f'{self.path}log/{glo.Today}.log', format='%(levelname)s :%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

if __name__ == '__main__':
    PATH = "./"
    Log(PATH).log()
    logging.basicConfig(filename=f'./log/{glo.Today.strftime("%Y-%m-%d")}.log', format="%(levelname)s :%(asctime)s %(message)s", encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like resund and Malmö')

    print(" ")
