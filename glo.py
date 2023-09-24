# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: glo.py
@Date ：2023/9/22 14:04
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
import datetime
from datetime import date

"""
全局数据
"""
class glo:
    login = "登录"
    sign = "打卡"
    success = "成功"
    error = "失败"
    Today = date.today()

# 如果是周末打卡则在考勤范围
def isWeekend(Today):
    ret = 0

    # 仅支持星期六数据
    if Today.isoweekday() == 6:
        ret = 1

    return ret

if __name__ == '__main__':
    print(isWeekend(glo.Today))