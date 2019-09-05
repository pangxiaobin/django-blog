#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-7-4 下午5:55
# @Author  : Hubery
# @File    : helper.py
# @Software: PyCharm

import time
import requests
from requests.exceptions import ConnectionError

from HuberyBlog.settings import BASE_HEADERS


def retry(max_tries=3, wait=5):
    """
    失败重试
    :param max_tries: 最大重试次数
    :param wait: 失败后间隔时间
    :return:
    """
    def deco(fun):
        def wrapper(*args, **kwargs):
            for i in range(max_tries):
                result = fun(*args, **kwargs)
                if result is None:
                    print('retry%s' %i)
                    time.sleep(wait)
                    continue
                else:
                    return result
        return wrapper
    return deco


@retry()
def get_text(url, options={}):
    """
    :param method: 请求方法
    :param url: 请求的目标url
    :param options:添加的请求头
    :return:
    """
    headers = dict(BASE_HEADERS, **options)
    print('正在抓取', url)
    try:
        res = requests.get(url, headers=headers, timeout=5)
        # print(res.status_code)
        if res.status_code == 200:
            print('抓取成功', url, res.status_code)
            return res
    except ConnectionError:
        print('抓取失败', url)
        return None
