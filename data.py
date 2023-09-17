# -*- coding: UTF-8 -*-
"""
@Project: Project
@File: data.py
@Date ：2023/9/4 16:05
@Author：Amlei
@version：python 3.11
@IDE: PyCharm 2023.2
"""

"""
全局数据
"""
class glo():
    login = "登录"
    sign = "打卡"
    success = "成功"
    error = "失败"

"""
登录网址
"""
class URL():
    loginURL = ""   # 登录地址
    signURL = ""    # 打卡地址

    # 自行查看本机的头文件
    header = {
        "User-Agent": "",
        "Cookie": "",
        "Accept": ""
    }

"""
用户信息    已更改为MySQL数据库获取
"""
class user():
    # ZFTAL_CSRF_TOKEN -> 数据需抓包获取
    user = {
        "ZFTAL_CSRF_TOKEN": '',
        "yhm": "",  # 用户名
        "mm": ""  # 密码
    }

    # 用户id: 每个账号都是唯一的，需抓包获取
    id = ""

"""
地点信息  已更改为MySQL数据库获取
"""
class state():
    # 数据获取: https://api.map.baidu.com/lbsapi/getpoint/
    # 建议经纬度为六位小数，能够匹配打卡信息
    longitude = 0  # 打卡经度
    latitude = 0  # 打卡维度
    location = ""  # 打卡地点

    # 如果你已填报实习地点，并且获取的经纬度为实习地点附近，需将 'zkqfw'类型更改为1
    datas = {
        "mbjd": "{:.2f}".format(longitude - 0.75),
        "mbwd": "{:.2f}".format(latitude + 0.65),
        "yxwc": 500,
        "kqjd": longitude,
        "kqwd": latitude,
        "kqddxx": location,
        "rwxm_id": user.id,  # 用户id: 每个账号都是唯一的，需抓包获取
        "kqlx": 0,   # 考勤类型: 0 -> 签到,1 -> 签退
        "zkqfw": 1,  # 在考勤范围: 0 -> 否, 1 -> 是
    }

if __name__ == '__main__':
    print(user.user)
