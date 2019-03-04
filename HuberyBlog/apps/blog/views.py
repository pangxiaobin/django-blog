from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from blog.models import Wheels, Blog, Tag, Category, WebCategory

from blog.helper import page_cache

# from asynchronous_send_mail import send_mail


# from django.core.mail import send_mail
@page_cache(10)
def home(request):
    """
     首页
     :param request:
     :return:
     """
    wheels = Wheels.objects.all().order_by('-id')
    if wheels.count() >= 4:
        wheels = wheels[:4]
    blogs = Blog.objects.all().order_by('-create_time')
    tags = Tag.objects.all()
    data = {
        'tittle': '首页',
        'wheels': wheels,
        'blogs': blogs,
        'tags': tags
    }
    return render(request, 'blog/home.html', context=data)


def get_all_blog(request):
    """
    返回所有的博客
    :param request:
    :return:
    """
    blogs = Blog.objects.all().order_by('-create_time')
    data = {
        'title': '全部博客',
        'blogs': blogs
    }
    return render(request, 'blog/blog_list.html', context=data)


def create_blog(request):
    pass


# @page_cache(10)
def read_blog(request):
    """
    阅读博客
    :param request:
    :return:
    """
    try:
        blog_id = request.GET.get('blogid')
        blog = Blog.objects.filter(pk=blog_id).first()
        pre_blog = Blog.objects.filter(id__lt=blog.id).order_by('-id')
        next_blog = Blog.objects.filter(id__gt=blog.id).order_by('id')
        # 取第1条记录
        if pre_blog.count() > 0:
            pre_blog = pre_blog[0]
        else:
            pre_blog = None

        if next_blog.count() > 0:
            next_blog = next_blog[0]
        else:
            next_blog = None
        if not request.COOKIES.get('blog_%s_readed' % blog_id):
            read_num = blog.read_num + 1
            blog.read_num = read_num
            blog.save()
        data = {
            'title': '博客详情',
            'blog': blog,
            'pre_blog': pre_blog,
            'next_blog': next_blog
        }
    except Blog.DoesNotExist:
        raise Http404
    response = render(request, 'blog/read_blog.html', context=data)
    response.set_cookie('blog_%s_readed' % blog_id, "True")
    return response


def get_categories(request):
    """
    返回对应分类下的所以文章
    :param request:
    :return:
    """
    category_name = request.GET.get('category_name')
    category = Category.objects.filter(name=category_name).first()
    blogs = category.blog_set.all().order_by('-create_time')
    data = {
        'title': category_name,
        'blogs': blogs
    }
    return render(request, 'blog/blog_list.html', context=data)


def search_blog(request):
    """
    搜索文章
    :param request:
    """
    key_word = request.POST.get('key_word')
    if key_word == '':
        return redirect(reverse('blog:get_all_blog'))
    search_blogs = Blog.objects.filter(title__contains=key_word).order_by('-create_time')
    data = {
        'title': '搜索结果',
        'blogs': search_blogs
    }
    return render(request, 'blog/blog_list.html', context=data)


def get_tags(request):
    """
    返回对应标签下的所以博客
    :param request:
    """
    tag_id = request.GET.get('tag_id')
    tag = Tag.objects.filter(pk=tag_id).first()
    blogs = tag.blog_set.all()
    data = {
        'title': tag.name,
        'blogs': blogs
    }
    return render(request, 'blog/blog_list.html', context=data)


# def test_email(request):
#     subject = '这是djiango邮件发送测试'
#     message = '这是测试内容'
#     frome_mail = '1456819312@qq.com'
#     recipient_list = ['2274858959@qq.com']
#     html = '<h1 style="color: red">没有查到相关博客</h1>'
#     try:
#         send_mail(subject, message, frome_mail, recipient_list, fail_silently=False, html_message=html)
#         return HttpResponse('发送成功')
#     except Exception as e:
#         print(e)
#         return HttpResponse('发送失败')
def web_nav(request):
    """
    网站导航
    :param request:
    :return:
    """
    web_categories = WebCategory.objects.all()
    data = {
        'title': '网站导航',
        'web_categories': web_categories
    }
    return render(request, 'blog/web_navigation.html', context=data)


def archives(request):
    """
    文章归档
    :param request:
    :return:
    """
    dates = Blog.objects.all()
    data = {
        'title': '文章归档',
        'dates': dates
    }
    return render(request, 'blog/archives.html', context=data)