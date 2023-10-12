# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: glo.py
@Date ：2023/9/22 14:04
@Author：Amlei
@version：python 3.12
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
    report = "周报"
    success = "成功"
    error = "失败"
    festival = "假期"
    Today = date.today()

# 如果是周末打卡则在考勤范围
def today_is_weekend() -> int:
    ret: int = 0

    # 仅支持星期六数据
    if glo.Today.isoweekday() == 6:
        ret = 1

    return ret

def date_is_holiday(date: datetime) -> bool:
    ret: bool = False

    try:
        assert is_holiday(date) is False
    except AssertionError:
        ret = True

    return ret


def log_info(context: str) -> None:
    logging.info(context)
    print(context)


def log_error(context: str) -> None:
    logging.error(context)
    print(context)


def log_waring(context: str) -> None:
    logging.warning(context)
    print(context)

if __name__ == '__main__':
    # print(today_is_weekend())

    if (today_is_holiday() == True):
        print("1")