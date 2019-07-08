#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-7-5 下午3:17
# @Author  : Hubery
# @File    : adminx.py
# @Software: PyCharm

import xadmin

from hot.models import Hot


class HotAdmin(object):
    """热榜"""
    list_display = ['hot_name', 'create_time', 'status']
    search_fields = ['name']


xadmin.site.register(Hot, HotAdmin)