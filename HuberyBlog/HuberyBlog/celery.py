#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-6 下午3:43
# @Author  : Hubery
# @File    : celery.py
# @Software: PyCharm

from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HuberyBlog.settings')

app = Celery('HuberyBlog')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.update(
#     CELERYBEAT_SCHEDULE= {
#         'sum-task': {
#             'task': 'blog.tasks.get_all_visit_num',  # 定时任务 获取在线人数
#             'schedule':  crontab(),
#             'args': (),
#         }
#     }
# )
