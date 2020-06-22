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


def get_ip_address_from_taobao(ip):
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
        print('请求淘宝地址失败, 失败原因{}'.format(e))
        return None


def get_ip_address_from_pconline(ip):

    url = 'http://whois.pconline.com.cn/ipJson.jsp?ip={}&json=true'.format(ip)
    headers = BASE_HEADERS
    try:
        res = requests.get(url, headers=headers, timeout=5)
        addr = res.json().get('addr', None)
        if addr:
            ip_address = '/'.join(addr.split(' '))
        else:
            ip_address = None
        return ip_address
    except Exception:
        return None


def get_ip_from_ip_api(ip):

    url = 'http://ip-api.com/json/{}?lang=zh-CN'.format(ip)
    headers = BASE_HEADERS
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res_json = json.loads(res.json())
        print(res_json)
        if res_json.get('status') == 'success':
            country = res_json.get('country')
            city = res_json.get('city')
            regionName = res_json.get('regionName')
            ip_address = '/'.join([country, city, regionName])
            return ip_address
        return None
    except Exception:
        return None


def get_ip_from_alaip(ip):

    url = 'https://v1.alapi.cn/api/ip/?ip={}'.format(ip)
    headers = BASE_HEADERS
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res_json = res.json()
        if res_json.get('code') == 200:

            ad_info = res_json.get('data').get('ad_info')
            nation = ad_info.get('nation')
            province = ad_info.get('province')
            city = ad_info.get('city')
            district = ad_info.get('district')
            ip_address = '/'.join([nation, province, city, district])
            return ip_address
        return None
    except Exception as e:
        return None


def get_ip_address(ip):
    get_ip_func_list = [get_ip_from_alaip, get_ip_from_ip_api, get_ip_address_from_pconline, get_ip_address_from_taobao]
    for get_ip_func in get_ip_func_list:
        ip_address = get_ip_func(ip)
        if ip_address:
            return ip_address
    return None


def get_ip(request):
    """
    获取ip
    :param request:
    :return:
    """
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


if __name__ == '__main__':

    ip = get_ip_address('127.0.0.1')
    print(ip)
