# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: sql.py
@Date ：2023/9/16 21:09
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
import logging
import pprint
import pymysql
import datetime
from glo import glo

# from data import glo
# from log import Log

# Log("/home/test/code/python/ZF-Internship/HTTP/").log()     # # Aliyun Server PATH

class SQL():
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='123456', database='zf_internship')
        self.cursor = self.db.cursor()
        self.data = {"state": {}, "user": {}}

    # 插入打卡数据
    def insert(self, table:str=None, token:str=None, user:int=None, password:str=None, mail:str=None, longitude:float=None, latitude:float=None, location:str=None):
        """
        table: 仅提供state、user表
        """
        if table == 'state':
            self.cursor.execute(
                f"insert into state(mbjd, mbwd, kqjd, kqwd,kqddxx) values ({'{:.2f}'.format(longitude - 0.75)},{'{:.2f}'.format(latitude + 0.65)},'{longitude}','{latitude}','{location}')")
        elif table == 'user':
            self.cursor.execute(
                f"insert into user values ('{token}','{user}','{password}','{mail}')")
        else:
            exit()
        self.db.commit()
        return self.cursor

    # 查询表数据
    def select(self, table:str):
        self.cursor.execute(f"select * from {table}")
        return self.cursor.fetchall()

    # 加载需要登录、签到的信息
    def updateData(self, table: str, property:list):
        tableData = self.select(table)

        for i in range(self.count('user')):
            self.data[table][i + 1] = {}
            for j in range(len(property)):
                self.data[table][i + 1][property[j]] = tableData[i][j + 1]

        return self.data

    # 统计表数据条目
    def count(self, table):
        self.cursor.execute(f"select count(*) from {table}")
        return self.cursor.fetchall()[0][0]

    # 关闭数据库连接
    def close(self):
        self.db.close()

# 继承父类
class reportSQL(SQL):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def insert(self, year: int, reports: list):
        date = datetime.date.today()
        reportLen = len(reports)
        count = 0  # 周记数据条目
        zc_h_zj = 15  # 系统默认递增周次
        zc = 4  # 打卡周次

        while date.year == year:  # 循环直到年份不再是指定年份
            if date.weekday() == 5 and 0 < reportLen:  # 如果是星期六
                try:
                    self.cursor.execute(
                        f"insert into report(zc_h_zj, xh_id, xzc, zc, rzqssj, rzjssj, zrznr) values({zc_h_zj},{self.user},{zc_h_zj},{zc},'{'{}-{:02}-{:02}'.format(date.year, date.month, date.day - 5)}','{date.strftime('%Y-%m-%d')}','{reports.pop(0)}');")
                    self.db.commit()
                except:
                    print("插入周报出错")
                zc_h_zj += 1
                zc += 1
                count += 1
                reportLen -= 1
                # print(date)
            date += datetime.timedelta(days=1)  # 递增日期

        return count

    def select(self, today: datetime.date):
        self.cursor.execute(f"select * from report where xh_id = {self.user} and rzjssj='{today}'")

        return self.cursor.fetchall()

    def updateData(self, property:list):
        self.data = {}

        datas = self.select(glo.Today)
        # print(data)
        try:
            for j in range(len(property)):
                # 将None数据更改为空
                data = datas[0][j + 1]
                if (data == None):
                    data = ""
                self.data[property[j]] = data
        except IndexError:
            print("数据为空！")

        return self.data

def execute():
    db = SQL()
    stateProperty = ['mbjd', 'mbwd', 'yxwc', 'kqjd', 'kqwd', 'kqddxx', 'rwxm_id', 'kqlx', 'zkqfw']
    userProperty = ['ZFTAL_CSRF_TOKEN', 'yhm', 'mm']

    db.updateData('user', userProperty)
    db.updateData('state', stateProperty)

    del stateProperty, userProperty

    db.close()
    return db


if __name__ == '__main__':
    # pprint.pprint(execute().data)
    report = open("./report.txt", "r", encoding="utf-8").read().split("===")

    reportProperty = ['zrzlx', 'ywlyb', 'id1', 'sxwd', 'kcsxwd', 'zc_h_zj', 'yf_h_zj', 'sfbx', 'xh_id', 'zjId', 'ksrq', 'jsrq', 'sxxx', 'xzc', 'zc', 'autocomplete', 'rzqssj', 'rzjssj', 'zrznr', 'ewzrznr', 'file', 'fjxx', 'ywbjKey']
    reSQL = reportSQL(2104230114)
    # reSQL.insert(2023)

    a = reSQL.updateData(reportProperty)
    # pprint.pprint(a)
    # reSQL.insert(2023, report)
    reSQL.close()

