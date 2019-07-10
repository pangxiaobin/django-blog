#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-1-24 下午4:04
# @Author  : Hubery
# @File    : helper.py
# @Software: PyCharm

import json
import requests

from django.core.cache import cache

from HuberyBlog.settings import BASE_HEADERS


def page_cache(timeout):
    def wrapper1(view_func):
        def wrapper2(request):
            key = 'PageCache-%s' % request.get_full_path()
            response = cache.get(key)
            if response is None:
                response = view_func(request)
                cache.set(key, response, timeout)
            return response

        return wrapper2

    return wrapper1


def get_ip_address(ip):
    """
    获取ip地址
    :param ip:
    :return:
    """
    url = 'http://ip.taobao.com//service/getIpInfo.php?ip={}'.format(ip)
    headers = BASE_HEADERS
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            res_dict_data = json.loads(res.text).get('data', '')
            country = res_dict_data.get('country', '')
            region = res_dict_data.get('region', '')
            city = res_dict_data.get('city', '')
            isp = res_dict_data.get('isp', '')
            ip_address = '/'.join([country, region, city, isp])
            return ip_address
        else:
            return ''
    except Exception as e:
        print('请求淘宝地址失败, 失败失败原因{}'.format(e))
        return None