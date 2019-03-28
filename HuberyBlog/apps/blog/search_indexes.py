#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-27 下午4:52
# @Author  : Hubery
# @File    : search_indexes.py
# @Software: PyCharm

from haystack import indexes
from blog.models import Blog


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        return self.get_model().objects.all()