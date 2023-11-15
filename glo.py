# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: glo.py
@Date ：2023/9/22 14:04
@Author：Amlei (lixiang.altr@qq.com)
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import datetime
import logging
from datetime import date
from time import sleep
import random
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
    today = date.today()
    null = 0
    insert_user = 1
    insert_state = 2
    update_data = 3

# 如果是周末打卡则在考勤范围
def today_is_weekend() -> bool:
    ret: bool = False

    # 仅支持星期六数据
    if glo.today.isoweekday() == 6:
        ret = True

    return ret


def date_is_holiday(now_date: datetime) -> bool:
    ret: bool = False

    try:
        assert is_holiday(now_date) is False
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

def self_sleep(start: int, end: int, text: str = None) -> None:
    dormancy: float = float("{:.2f}".format(random.uniform(start, end)))
    print(f"{text}, 休眠{dormancy}秒")
    sleep(dormancy)


if __name__ == '__main__':
    # print(today_is_weekend())
    # 若今天为第一天假期  date_is_holiday(glo.Today - datetime.timedelta(days=1)) == False)
    if date_is_holiday(glo.today) is True and date_is_holiday(glo.today - datetime.timedelta(days=1)) is False:
        print("今日是假期，停止打卡")
        logging.info("今日是假期，停止打卡")
    elif date_is_holiday(glo.today) is True and date_is_holiday(glo.today + datetime.timedelta(days=1)) is True:
        print("今明均为假期, 直接退出程序不发送邮件提醒")
        logging.info("今日是假期，停止打卡")

