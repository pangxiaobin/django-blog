#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-1-17 下午4:08
# @Author  : Hubery
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url

from blog import views
from blog.search_view import MySearchView

urlpatterns = [
    url(r'^read/$', views.read_blog, name='read_blog'),
    url(r'^get_all_blog/$', views.get_all_blog, name='get_all_blog'),
    url(r'^get_categories/$', views.get_categories, name='get_categories'),
    url(r'^get_tags/$', views.get_tags, name='get_tags'),
    url(r'^search/$', MySearchView(), name='haystack'),
    # url(r'^test_email/$', views.test_email),
    url(r'^web_nav/$', views.web_nav, name='web_nav'),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^message_board/$', views.message_board, name='message_board'),
    url(r'^about/$', views.about, name='about'),
    url(r'^get_online_ips/$', views.get_online_ips, name='get_onlines_ips'),
    url('^return_ip/$', views.return_ip),
    url('^sponsor/$', views.sponsor, name='sponsor'),

]

