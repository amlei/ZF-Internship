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
import function.data
from datetime import date
from time import sleep
from random import choices
from random import uniform
from chinese_calendar import is_holiday


class Glo:
    """ 全局数据 (不可更改) """
    login: str = "登录"
    sign: str = "打卡"
    sing_out: str = "签退"
    report: str = "周报"
    success: str = "成功"
    error: str = "失败"
    festival: str = "假期"
    log: str = "日志"
    today: datetime = date.today()
    null: int = 0
    insert_user: int = 1
    insert_state: int = 2
    update_data: int = 3
    sing_out_time: int = 18
    start_time: list[int] = [100, 150, 200, 250, 300, 350, 400, 450]
    end_time: list[int] = [200, 300, 400, 500, 600, 700, 800, 900]

# 如果是周末打卡则在考勤范围
def today_is_weekend() -> bool:
    ret: bool = False

    # 仅支持星期六数据
    if Glo.today.isoweekday() == 6:
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

    function.data.send_log += f"{context}\n"
    print(context)


def log_error(context: str) -> None:
    logging.error(context)
    function.data.send_log += f"{context}\n"
    print(context)


def log_waring(context: str) -> None:
    logging.warning(context)
    # data.send_log += f"{context}\n"
    print(context)

def self_sleep(start: int, end: int, text: str = None) -> None:
    dormancy: float = float("{:.2f}".format(uniform(start, end)))
    print(f"{text}, 休眠{dormancy}秒")
    sleep(dormancy)

def random_time() -> list:
    """ 随机选择时间 """
    while True:
        start_sleep = choices(Glo.start_time)[0]
        end_sleep = choices(Glo.end_time)[0]
        # 结束时间一定要比开始时间大
        if start_sleep < end_sleep:
            break
    return [start_sleep, end_sleep]

if __name__ == '__main__':
    # print(today_is_weekend())
    # 若今天为第一天假期  date_is_holiday(glo.Today - datetime.timedelta(days=1)) == False)
    # if date_is_holiday(glo.today) is True and date_is_holiday(glo.today - datetime.timedelta(days=1)) is False:
    #     print("今日是假期，停止打卡")
    #     logging.info("今日是假期，停止打卡")
    # elif date_is_holiday(glo.today) is True and date_is_holiday(glo.today + datetime.timedelta(days=1)) is True:
    #     print("今明均为假期, 直接退出程序不发送邮件提醒")
    #     logging.info("今日是假期，停止打卡")

    """ 测试随机选择 """
    r = random_time()
    s = r.pop(0)
    e = r.pop(0)
    print(s, e)