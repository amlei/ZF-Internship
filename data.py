# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: data.py
@Date ：2023/9/4 16:05
@Author：Amlei
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import pprint
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
# 执行用户数据操作
def userExecute(user: int):
    db = SQL()
    db.user(user)
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

    match option:
        # 插入周报
        case True:
            # 拿出当前最新周报数据周次值
            zc = reSQL.in_current_week()
            # 最新周次 + 1
            reSQL.insert(2023, zc.pop(0) + 1, zc.pop(0) + 1)
        # 从数据库传入周报数据
        case False:
            reSQL.user(user)
            reSQL.updateData()
    reSQL.close()

    return reSQL

if __name__ == '__main__':
    a = reportExecute(学号)
    pprint.pprint(a)
