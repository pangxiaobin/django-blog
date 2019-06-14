#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-6-14 下午2:47
# @Author  : Hubery
# @File    : blog_sitemap.py
# @Software: PyCharm

from django.contrib.sitemaps import Sitemap

from blog.models import Blog


class BlogSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.create_time

    def location(self, obj):
        return '/blog/read/?blogid={}'.format(obj.id)
