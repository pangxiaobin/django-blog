#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-1-18 上午10:50
# @Author  : Hubery
# @File    : adminx.py
# @Software: PyCharm
from django.contrib.sites.models import Site

import xadmin
from xadmin import views
from blog.models import Blog, Wheels, Tag, Category, WebCategory, Web, MessageBoard, VisitView, FriendsBlog, Soul, BlockIP

class BlogAdmin(object):
    """博客文章"""
    list_display = ['id','title', 'contents', 'read_num', 'appreciate', 'create_time', 'show_all_tags', 'categoryid']
    search_fields = ['title']
    readonly_fields = ['read_num']
    style_fields = {'content': 'ueditor'}

    def show_all_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class WheelsAdmin(object):
    """轮播图"""
    list_display = ['name', 'image', 'create_time']
    search_fields = ['name']


class TagAdmin(object):
    """标签"""
    list_display = ['name']
    search_fields = ['name']


class CategoryAdmin(object):
    """分类"""
    list_display = ['name', 'create_time']
    search_fields = ['name']


class WebCategoryAddmin(object):
    """网站分类"""
    list_display = ['name', 'create_time']
    search_fields = ['name']


class WebAdmin(object):
    """网站地址"""
    list_display = ['name', 'net_address', 'create_time', 'web_category']
    search_fields = ['name']


class MessageBoardAdmin(object):
    """网站地址"""
    list_display = ['id', 'name', 'create_time']
    search_fields = ['name']


class VisitViewAdmin(object):
    """访问统计"""
    list_display = ['id', 'ip', 'ip_address', 'visit_num', 'first_visit_time', 'last_visit_time']
    search_fields = ['ip']
    readonly_fields = ['visit_num']


class FriendsBlogAdmin(object):
    """友情链接"""
    list_display = ['id', 'name', 'address', 'status', 'create_time']
    search_fields = ['name']


class SoulAdmin(object):
    list_display = ['id', 'title', 'hits']


class SiteAdmin(object):
    """
    用于修改站点地图里面的域名
    """
    list_display = ['id', 'domain']


class BlockIPAdmin(object):
    """ip 黑名单"""
    list_display = ['id', 'ip', 'status']


class BaseSetting(object):
    enable_themes = True  # 开启自定义主题
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "HuberyBlog"
    site_footer = "hubery blog"
    menu_style = "accordion"



xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(Wheels, WheelsAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(WebCategory, WebCategoryAddmin)
xadmin.site.register(Web, WebAdmin)
xadmin.site.register(MessageBoard, MessageBoardAdmin)
xadmin.site.register(VisitView, VisitViewAdmin)
xadmin.site.register(FriendsBlog, FriendsBlogAdmin)
xadmin.site.register(Soul, SoulAdmin )
xadmin.site.register(Site, SiteAdmin)
xadmin.site.register(BlockIP, BlockIPAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
