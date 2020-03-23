#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-6 下午8:52
# @Author  : Hubery
# @File    : pv_middleware.py
# @Software: PyCharm
import re
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from HuberyBlog.settings import EXCLUDE_URL
from blog.tasks import increase_pv


class PvVisitViewMiddleware(MiddlewareMixin):
    """统计在线人数和用户访问"""
    def process_request(self, request):
        if request.path not in EXCLUDE_URL and not re.match(r'^.*xadmin.*$', request.path):
            ip = get_ip(request)
            online_ips = cache.get("online_ips", [])
            if online_ips:
                # 根据取出的ip list获取缓存中仍然存在的ip
                online_ips = list(cache.get_many(online_ips).keys())
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


class CleanCacheMiddleware(MiddlewareMixin):
    """当访问当路径包含　xadmin/blog 且method 方法为post时，清空首页缓存"""
    def process_request(self, request):
        if re.match( r'^.*xadmin.*$', request.path) and request.method == "POST":
            key = 'PageCache-%s' % '/'
            cache.delete(key)

        #  提交评论时　更新阅读页缓存
        if re.match(r'^.*comments/post.*$', request.path) and request.method == 'POST':
            data = request.POST.copy()
            key = 'PageCache-%s' % data.get('next', '')
            cache.delete(key)


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