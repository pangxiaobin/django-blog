#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-6 下午3:13
# @Author  : Hubery
# @File    : tasks.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals


from celery import shared_task

from django.db.models import F
from blog.models import Blog, VisitView

@shared_task
def increase_uv(blog_id):
    """
    异步增加阅读数
    :param blog_id: 博客的id
    :return:
    """
    return Blog.objects.filter(id=blog_id).update(read_num=F('read_num')+1)


@shared_task
def increase_pv(ip):
    """如果获取到了对于ip 就在这个基础上加一,没有新建一个"""
    visits = VisitView.objects.filter(ip=ip)
    if visits.count() == 0:
        visit_ = VisitView.objects.create(ip=ip, visit_num=1)
        return 'success create %s' % ip
    visit = visits.first()
    visit.visit_num += 1
    visit.save()
    return 'success save %s' % ip


# @shared_task
# def get_all_visit_num():
#     """获取总的访问次数"""
#     visits_nums = VisitView.objects.aggregate(Sum("visit_num")).get('visit_num__sum', 0)
#
#     return visits_nums