#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-7-5 下午3:40
# @Author  : Hubery
# @File    : tasks.py
# @Software: PyCharm

import sys
import os
import django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.update({"DJANGO_SETTINGS_MODULE": "HuberyBlog.settings"})
django.setup()


# from __future__ import absolute_import, unicode_literals

from concurrent.futures import ThreadPoolExecutor

from celery import shared_task
from hot.crawler import *
from hot.models import Hot


@shared_task
def run_crawler():
    """
    定时一个小时更新一次爬取
    :return:
    """
    crawler_list = [crawler_zhi_hu, crawler_v2ex, crawler_github, crawler_wei_bo, crawler_tie_ba, crawler_dou_ban,
                    crawler_tian_ya, crawler_wang_yi]

    with ThreadPoolExecutor(max_workers=4) as pool:

        def get_result(future):
            """
            这个是 add_done_callback()方法来添加回调函数,
            future.result()为函数运行的结果
            :param future:
            :return:
            """
            crawler_result = future.result()
            hot_name = crawler_result.get('hot_name', '')
            content = crawler_result.get('content', '')
            if hot_name:
                hot = Hot.objects.filter(hot_name=hot_name).first()
                if not hot:
                    pass
                    Hot.objects.create(hot_name=hot_name, content=content)
                else:
                    hot.content = content
                    hot.save()
        for future in crawler_list:
            pool.submit(future).add_done_callback(get_result)
    print('done')


if __name__ == '__main__':
    run_crawler()