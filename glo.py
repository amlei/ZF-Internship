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
import logging
from datetime import date
from chinese_calendar import is_holiday

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
def today_is_weekend():
    ret = 0

    # 仅支持星期六数据
    if glo.Today.isoweekday() == 6:
        ret = 1

    return ret

def today_is_holiday():
    ret = False

    try:
        assert is_holiday(glo.Today) is False

    except AssertionError:
        ret = True
        print("今日是假期，停止打卡")
        logging.error("今日是假期，停止打卡")

    return ret

if __name__ == '__main__':
    # print(today_is_weekend())

    if (today_is_holiday() == True):
        print("1")