# -*- coding: UTF-8 -*-
"""
@Project: log.py
@File: state.py
@Date ：2023/10/11 20:37
@Author：Amlei (lixiang.altr@qq.com)
@version：python 3.12
@IDE: PyCharm 2023.2
"""
import json
import pprint
from typing import Any
import requests

# 地理编码
def geocode() -> dict[str, float | Any]:
    """
    输入地址规则遵循：国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦，如：北京市朝阳区阜通东大街6号。
    """
    # address = map(str, input("请输入打卡地址:").split(" "))
    address: str = input("请输入打卡地址:")
    # 参数参考: https://lbs.amap.com/api/webservice/guide/api/georegeo/
    geo_url = f"https://restapi.amap.com/v3/geocode/geo?parameters&key={}&address={address}"
    if address != "":
        data = requests.get(geo_url)
        # 打卡经纬度
        location = [float(i) for i in
                    json.loads(data.text)['geocodes'][0]['location'].split(",")]
        # 打卡地址 只保留省与市以下地址
        sign_address = json.loads(data.text)['geocodes'][0]['formatted_address'].replace(f"{json.loads(data.text)['geocodes'][0]['province']}{json.loads(data.text)['geocodes'][0]['city']}", "")

        return dict(longitude=float(location[0]), latitude=float(location[1]), address=sign_address)
    else:
        print("输入地址空!")

if __name__ == '__main__':
    a = geocode()
    pprint.pprint(a)
