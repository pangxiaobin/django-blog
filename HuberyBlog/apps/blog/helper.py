#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-1-24 下午4:04
# @Author  : Hubery
# @File    : helper.py
# @Software: PyCharm

from django.core.cache import cache


def page_cache(timeout):
    def wrapper1(view_func):
        def wrapper2(request):
            key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            if response is None:
                response = view_func(request)
                cache.set(key, response, timeout)
            return response

        return wrapper2

    return wrapper1