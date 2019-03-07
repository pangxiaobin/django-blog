#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-6 下午8:52
# @Author  : Hubery
# @File    : pv_middleware.py
# @Software: PyCharm
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from blog.tasks import increase_pv


class PvVisitViewMiddleware(MiddlewareMixin):
    """统计在线人数和用户访问"""
    def process_request(self, request):
        ip = get_ip(request)
        online_ips = cache.get("online_ips", [])
        cache.set(ip, 0, 1 * 60)
        if ip not in online_ips:
            online_ips.append(ip)
        cache.set("online_ips", online_ips)

    def process_response(self, request, response):
        ip = get_ip(request)
        if not request.COOKIES.get('visit_ip_%s' % ip):
            increase_pv.delay(ip)
            response.set_cookie('visit_ip_%s' % ip, 'True')  # 默认关闭浏览器过期
        return response


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