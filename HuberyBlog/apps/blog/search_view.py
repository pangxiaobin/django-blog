#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-3-28 上午11:20
# @Author  : Hubery
# @File    : search_view.py
# @Software: PyCharm

from haystack.views import SearchView
from blog.models import Blog


class MySearchView(SearchView):

    def build_page(self):
        return None

    def get_context(self):
        results = self.results
        # 当全文找不到时 走这个
        if results.__len__() <= 0:
            print('sda')
            results = []
            key_word = self.query
            search_blogs = Blog.objects.filter(title__icontains=key_word).order_by('-create_time')
            for search_blog in search_blogs:
                results.append({"object": search_blog})
        context = {
            'title': '博客搜索',
            'query': self.query,
            'form': self.form,
            'suggestion': None,
            'results': results

        }
        if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        return context
