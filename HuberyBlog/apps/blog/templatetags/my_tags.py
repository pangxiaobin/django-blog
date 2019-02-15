#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-1-24 上午11:37
# @Author  : Hubery
# @File    : my_tags.py
# @Software: PyCharm

from django import template
from django.utils.html import format_html

from blog.models import Category, Blog

register = template.Library()


@register.assignment_tag()
def get_categories():
    """获取分类"""
    categories = Category.objects.all().order_by('-create_time')
    data_html = ''
    for category in categories:
        data_html += '<dd><a href="/blog/get_categories/?category_name={}">{}&nbsp;（{}）' \
                    '</a></dd>'.format(category.name, category.name, category.blog_set.count())
    return format_html(data_html)


@register.assignment_tag()
def get_top_blog():
    """获取热榜"""
    blogs = Blog.objects.all().order_by('-read_num', '-create_time')[:10]
    data_html = ''
    for i in range(len(blogs)):
        blog = blogs[i]
        data_html += ' <li><strong><a href="/blog/read/?blogid={}">{}、{}</a></strong>' \
                     '</li>'.format(blog.id, i, cut_char(blog.title))
    return format_html(data_html)


@register.assignment_tag()
def get_random_blog(except_id=0):
    """获取随机推荐"""
    rand_count = 10
    rand_blogs = Blog.objects.exclude(id=rand_count).order_by('?')[:rand_count]
    data_html = ''
    for blog in rand_blogs:
        data_html += ' <li><strong><a href="/blog/read/?blogid={}">{}</a></strong>' \
                     '</li>'.format(blog.id, cut_char(blog.title))
    return format_html(data_html)


def cut_char(content):
    """只显示前20个字符"""
    if len(content) >= 20:
        return '%s%s' % (content[:20], '...')
    else:
        return content