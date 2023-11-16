# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: data.py
@Date ：2023/9/4 16:05
@Author：Amlei (lixiang.altr@qq.com)
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import json
import pprint
from datetime import date
from sql import SQL
from sql import reportSQL

"""
网址
"""
class URL:
    loginURL = ""  # 登录地址
    signURL = ""  # 打卡地址
    singPageUrl = ""  # 打卡页面地址
    singInfoUrl = ""  # 打卡信息地址
    reportURL = ""  # 周报上传地址


    # 自行查看本机的头文件
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.0.0",
        "Cookie": "JSESSIONID=598A5B294147291E7E361D1D1D99B2EB",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

# 执行用户数据操作
def userExecute(user: int):
    db = SQL()
    db.update_user(user)
    # 更新用户数据
    db.updateData('user')
    # 更新打卡数据
    db.updateData('state')

    db.close()
    return db

# 执行周报数据操作
def reportExecute(user: int, option: bool = False):
    """
    option: 默认为False -> 不执行插入操作
    **kwargs: 提供账号已打卡到的系统周次、当前插入周报时的账号打卡周次
    """
    # 加载数据库
    reSQL = reportSQL()
    reSQL.update_user(user)
    match option:
        # 插入周报
        case True:
            # 最新周次 + 1
            reSQL.insert()
        # 从数据库传入周报数据
        case False:
            reSQL.update_user(user)
            reSQL.updateData()
    reSQL.close()

    return reSQL

if __name__ == '__main__':
    a = reportExecute(学号, True)
    # report = open("./report.txt", "r", encoding="utf-8").read().split("===")
    # print(len(report.pop(0)))




