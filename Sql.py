# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: sql.py
@Date ：2023/9/16 21:09
@Author：YaPotato
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import logging
import pprint
import re

import pymysql
import datetime
from glo import glo
from state import geocode
from log import Log

# Log("/home/test/code/python/ZF-Internship/HTTP/").log()     # # Aliyun Server PATH
# Log("/home/ya/code/python/ZF-Internship/HTTP/").log()     # # Ubuntu Server PATH

class SQL():
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='123456', database='zf_internship')
        self.cursor = self.db.cursor()
        self.data = {'user': {}, 'state': {}}
        self.user = None

    # 插入打卡数据
    def insert(self, table: str = None, **kwargs):
        """
        table: 仅提供state、user表
        **kwargs -> password: str = None, mail: str = None,
                    longitude: float = None, latitude: float = None, location: str = None
                    
        user表所需: user, password, mail
        state表所需: user, longitude, latitude
        
        例如：
        SQL.insert(table='user', password=123, mail=1234)
        SQL.insert(table='state', user=123, mbjd=110.01, mbwd=110.01, kqjd=110.01, kqwd=110.01, kqddxx='北京西四环')

        a.user(**)
        a.insert(table='user', password=**, mail="**@qq.com")
        a.insert(table='state', longitude=state_data['longitude'], latitude=state_data['latitude'], address=state_data['address'])
        """
        try:
            match table:
                case 'state':
                    self.cursor.execute(
                        f"insert into state(yhm, mbjd, mbwd, kqjd, kqwd,kqddxx) "
                        f"values ('{self.user}',{'{:.2f}'.format(kwargs['longitude'] - 0.75)},"
                        f"{'{:.2f}'.format(kwargs['latitude'] + 0.65)},"
                        f"'{kwargs['longitude']}','{kwargs['latitude']}','{kwargs['address']}')")
                case 'user':
                    self.cursor.execute(
                        f"insert into user(yhm, mm, mail) values ('{self.user}',"
                        f"'{kwargs['password']}','{kwargs['mail']}')")
        except Exception as e:
            logging.warning(f"插入表错误{e}")
            print(f"插入表错误{e}")
            pass

        self.db.commit()
        return self.cursor

    # 查询表数据
    def select(self, table: str) -> list:
        self.cursor.execute(f"select * from {table} where yhm={self.user}")

        return list(self.cursor.fetchall()[0])

    # 加载需要登录、签到的信息
    def updateData(self, table: str) -> dict:
        # 提供不同的数据切片
        defSlice = None
        match table:
            case "user":
                # ['yhm', 'mm']
                defSlice = slice(2)
            case "state":
                # ['mbjd', 'mbwd', 'yxwc', 'kqjd', 'kqwd', 'kqddxx', 'rwxm_id', 'kqlx', 'zkqfw']
                defSlice = slice(9)
        # 表单(值)数据
        tableData = self.select(table)[1:]
        # 键数据
        propertys = self.show_property(table)[defSlice]

        # 插入数据
        while propertys:
            self.data[table][propertys.pop(0)[0]] = tableData.pop(0)

        return self.data

    # 统计表数据条目
    def count(self, table):
        self.cursor.execute(f"select count(*) from {table}")

        return self.cursor.fetchall()[0][0]

    # 罗列出所有用户
    def allUser(self) -> tuple:
        self.cursor.execute("select yhm, mail from user")

        return self.cursor.fetchall()

    # 设置用户名
    def update_user(self, user) -> None:
        self.user = user

    # 关闭数据库连接
    def close(self) -> None:
        self.db.close()

    # 查看数据库栏
    def show_property(self, table: str) -> list:
        self.cursor.execute(f"show columns from {table}")

        return list(self.cursor.fetchall()[1:])

# 继承父类
class reportSQL(SQL):
    def __init__(self):
        super().__init__()

    def insert(self, year: int, zc_h_zj: int, zc: int) -> int:
        """
        year:       周报年份
        reports:    周报内容
        zc_h_zj:    系统默认递增周次，为账号已打卡到的系统周次
        zc:         当前插入周报时的账号打卡周次
        """
        date = datetime.date.today()
        report = open("./report.txt", "r", encoding="utf-8").read().split("===")
        # 周记条数
        count: int = 0

        # 循环直到年份不再是指定年份
        while date.year == year:
            # 如果是星期六
            while date.weekday() == 5 and report:
                try:
                    self.cursor.execute(
                        f"insert into report(zc_h_zj, yhm, xzc, zc, rzqssj, rzjssj, zrznr)"
                        f"values({zc_h_zj},{self.user},{zc_h_zj},{zc},"
                        f"'{'{}-{:02}-{:02}'.format(date.year, date.month, date.day - 5)}',"
                        f"'{date.strftime('%Y-%m-%d')}','{report.pop(0)}');")
                    self.db.commit()
                except:
                    print("插入周报出错, 程序不再执行")
                    exit()
                zc_h_zj += 1
                zc += 1
            date += datetime.timedelta(days=1)  # 递增日期

        return count

    def select(self, today: datetime.date) -> list:
        self.cursor.execute(f"select * from report where yhm = {self.user} and rzjssj='{today}'")
        data: list = list()

        try:
            data = list(self.cursor.fetchall()[0][1:])
        except IndexError:
            pass

        return data

    def updateData(self) -> dict:
        self.data = {}
        datas = self.select(glo.Today)
        propertys = self.show_property("report")
        """
        ['zrzlx', 'ywlyb', 'id1', 'sxwd', 'kcsxwd', 'zc_h_zj', 'yf_h_zj', 'sfbx', 'xh_id', 'zjId', 'ksrq',
         'jsrq', 'sxxx', 'xzc', 'zc', 'autocomplete', 'rzqssj', 'rzjssj', 'zrznr', 'ewzrznr', 'file',
         'fjxx', 'ywbjKey']
        """
        try:
            while propertys:
                property = propertys.pop(0)[0]
                data = datas.pop(0)
                # 空数据转为空
                if (data == None):
                    data = ""
                # 判断类型
                if (isinstance(data, datetime.date) == True):
                    data = str(data)

                match property:
                    case "yhm":
                        property = "xh_id"

                self.data[property] = data

            return self.data
        except IndexError:
            print("本周周报数据为空,无法完成本周周报上传!")
            logging.error("本周周报数据为空,无法完成本周周报上传!")
            # 不退出，以供跳过本账号
            pass

    # 当前周报最新数据
    def in_current_week(self) -> list:
        self.cursor.execute(f"select MAX(xzc), MAX(zc) from report where yhm = {self.user}")

        return list(self.cursor.fetchall()[0])

if __name__ == '__main__':
    # a = reportSQL()
    # a.user(2104230114)
    # zc = a.in_current_week()
    # 最新周次 + 1
    # a.insert(2023, zc.pop(0) + 1, zc.pop(0) + 1)
    # print(a.select(glo.Today))
    # c = a.updateData(reportProperty)
    # c = a.updateData()
    # c = a.select("2023-10-14")
    # print(c)
    # pprint.pp(c)

    a = SQL()
    a.update_user(2104230161)

    # print(a.user)
    state_data = geocode()
    # a.insert(table='user', password=266735, mail="2535471951@qq.com")
    a.insert(table='state', longitude=state_data['longitude'], latitude=state_data['latitude'], address=state_data['address'])

    # c = a.updateData('user')
    # print(a.select('user'))
    # pprint.pprint(a.data)