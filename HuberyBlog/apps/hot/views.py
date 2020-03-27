from django.shortcuts import render

# Create your views here.
from hot.models import Hot
from blog.helper import page_cache


@page_cache(60*30)
def hot(request):
    """
    返回热点信息
    :param request:
    :return:
    """
    hot_queryset = Hot.objects.all().filter(status=1)
    data = {
        'title':'热点聚合',
        'hot_queryset': hot_queryset
    }
    return render(request, 'hot/hot.html', context=data)
