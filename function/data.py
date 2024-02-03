# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: data.py
@Date ：2023/9/4 16:05
@Author：Amlei (lixiang.altr@qq.com)
@version：python 3.12
@IDE: PyCharm 2023.2
"""
from function.sql import reportSQL
from function.sql import SQL

""" 全局日志，提供当次运行结果发送给拥有者 (可更改) """
send_log: str = ""


class URL:
    """ 网址、用户数据 """
    loginURL = ""       # 登录地址
    signURL = ""        # 打卡地址
    singPageUrl = ""    # 打卡页面地址
    singInfoUrl = ""    # 打卡信息地址
    reportURL = ""      # 周报上传地址

    # 自行查看本机的头文件
    header = {
        "User-Agent": "",
        "Cookie": "",
        "Accept": ""
    }


def userExecute(user: int):
    """
    执行用户数据操作
    """
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
    执行周报数据操作
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
