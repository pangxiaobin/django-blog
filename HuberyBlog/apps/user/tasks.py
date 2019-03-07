#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-6 下午3:13
# @Author  : Hubery
# @File    : tasks.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time


@shared_task
def task2():
    print('异步2任务开始')
    time.sleep(10)
    print('异步2任务结束')
