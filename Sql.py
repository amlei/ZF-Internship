# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: Sql.py
@Date ：2023/9/16 21:09
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""
import pprint
import pymysql

class SQL():
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='123456', database='zf_internship')
        self.cursor = self.db.cursor()
        self.data = {"state": {}, "user": {}}

    # 建议直接使用mysql操作，该功能待完善
    def insert(self, table:str=None, token:str=None, user:int=None, password:str=None, mail:str=None, longitude:float=None, latitude:float=None, location:str=None):
        """
        table: 仅提供state、user表
        """
        if table == 'state':
            self.cursor.execute(
                f"insert into state(mbjd, mbwd, kqjd, kqwd,kqddxx) values ({'{:.2f}'.format(longitude - 0.75)},{'{:.2f}'.format(latitude + 0.65)},{longitude}, {latitude},{str(location)})")
        elif table == 'user':
            self.cursor.execute(
                f"insert into user values ({token},{user},{password},{mail})")
        else:
            exit()
        self.db.commit()
        return self.cursor

    # 查询表数据
    def select(self, table:str):
        self.cursor.execute(f"select * from {table}")
        return self.cursor.fetchall()

    # 加载需要登录、签到的信息
    def updateData(self, table:str, property:list):
        tableData = self.select(table)

        for i in range(self.count()):
            self.data[table][i + 1] = {}
            for j in range(len(property)):
                self.data[table][i + 1][property[j]] = tableData[i][j + 1]

        return self.data

    # 统计表数据条目
    def count(self):
        self.cursor.execute("select count(*) from user")
        return self.cursor.fetchall()[0][0]

    # 关闭数据库连接
    def close(self):
        self.db.close()

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
    pprint.pprint(execute().data)
    del execute().data
    # print(SQL().count())

