# -*- encoding: utf-8 -*-
"""
@File    : client.py
@Time    : 2022/10/9 16:26
@Author  : Jahan
@Software: PyCharm
"""

import requests


def register():
    info = {"user": ['letian', 'letian2'], "password": "12345678"}
    r = requests.post("http://192.168.0.101:80/register", data=info)
    print(r.text)


def add():
    info = {"a": 1, "b": 2}
    r = requests.post("http://192.168.0.101:80/add", json=info)
    print(r.headers)
    print(r.text)


def upload_file():
    file_data = {'image': open('Lenna.jpg', 'rb')}
    user_info = {'info': 'Lenna'}
    r = requests.post("http://192.168.0.100:80/uploads", data=user_info, files=file_data)
    print(r.text)


if __name__ == '__main__':
    # add()
    upload_file()
