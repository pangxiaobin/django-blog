#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-1-17 下午4:08
# @Author  : Hubery
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^read/$', views.read_blog, name='read_blog'),
    url(r'^get_all_blog/$', views.get_all_blog, name='get_all_blog'),
    url(r'^get_categories/$', views.get_categories, name='get_categories'),
    url(r'^get_tags/$', views.get_tags, name='get_tags'),
    url(r'^search_blog/$', views.search_blog, name='search_blog'),
    url(r'^test_email/$', views.test_email)
]

