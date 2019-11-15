"""HuberyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

import xadmin
# from django.views.static import serve

from blog import views
from hot import views as hot_views
from HuberyBlog import settings
from blog.blog_sitemap import BlogSitemap

sitemaps = {
    'Blog': BlogSitemap
}


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls, name='xadmin'),
    url(r'^$', views.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),  # xadmin集成富文本编辑器
    # url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),  # 配置上传文件的访问处理函数
    url(r'^comments/', include('django_comments.urls')),  # 评论。
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap',),
    url(r'^hot/$', hot_views.hot, name='hot'),
    url(r'^get_soul/$', views.get_soul, name='get_soul'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 配置上传文件的访问处理函数
