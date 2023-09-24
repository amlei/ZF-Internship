# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: data.py
@Date ：2023/9/4 16:05
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
import pprint
from datetime import date
from sql import SQL
from sql import reportSQL

"""
网址
"""
class URL:
    loginURL = ""    # 登录地址
    signURL = ""        # 打卡地址
    reportURL = ""    # 周报上传地址

    # 自行查看本机的头文件
    header = {
        "User-Agent": "",
        "Cookie": "",
        "Accept": ""
    }

def userExecute(user: int):
    db = SQL()
    db.user(user)
    stateProperty = ['mbjd', 'mbwd', 'yxwc', 'kqjd', 'kqwd', 'kqddxx', 'rwxm_id', 'kqlx', 'zkqfw']
    userProperty = ['ZFTAL_CSRF_TOKEN', 'yhm', 'mm']

    db.updateData('user', userProperty)
    db.updateData('state', stateProperty)

    db.close()
    return db

def reportExecute(user: int):
    report = open("./report.txt", "r", encoding="utf-8").read().split("===")

    reportProperty = ['zrzlx', 'ywlyb', 'id1', 'sxwd', 'kcsxwd', 'zc_h_zj', 'yf_h_zj', 'sfbx', 'xh_id', 'zjId', 'ksrq',
                      'jsrq', 'sxxx', 'xzc', 'zc', 'autocomplete', 'rzqssj', 'rzjssj', 'zrznr', 'ewzrznr', 'file',
                      'fjxx', 'ywbjKey']

    reSQL = reportSQL()
    reSQL.user(user)
    reSQL.updateData(reportProperty)

    # reSQL.insert(2023, report, 15, 4)
    reSQL.close()

    return reSQL

if __name__ == '__main__':
    a = reportExecute(学号)
    pprint.pprint(a)
