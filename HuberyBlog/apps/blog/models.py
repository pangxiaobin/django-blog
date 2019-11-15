from django.db import models

from DjangoUeditor.models import UEditorField
from user.models import UserInfo


# Create your models here.


class Wheels(models.Model):
    """轮播图"""
    name = models.CharField(max_length=100, verbose_name="图片名字")
    image = models.ImageField(upload_to='wheel/image/', verbose_name='轮播图片')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=32, unique=True, verbose_name='标签')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True, unique=True, verbose_name="分类名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    """博客文章"""
    uid = models.ForeignKey(UserInfo, verbose_name='关联作者')
    title = models.CharField(max_length=128, verbose_name="标题")
    content = UEditorField(verbose_name="博客内容", width=700, height=400, imagePath="blog/ueditor/%(basename)s_%(datetime)s.%(extname)s",
                           filePath="blog/ueditor/%(basename)s_%(datetime)s.%(extname)s", default='')
    read_num = models.IntegerField(default=0, verbose_name="阅读次数")
    appreciate = models.IntegerField(default=0, verbose_name="点赞次数")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    categoryid = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='分类')

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def contents(self):
        """修改在后台显示的数据的长度"""
        if len(self.content) > 90:
            return '%s...' % self.content[:90]
        else:
            return self.content


class WebCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name='网站类别')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "网站类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Web(models.Model):
    STATUS = (
        (0, '无效'),
        (1, '有效')
    )
    name = models.CharField(max_length=64, verbose_name='网站名字')
    net_address = models.CharField(max_length=128, verbose_name='网站地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    web_category = models.ForeignKey(WebCategory, verbose_name='关联网站分类')
    status = models.SmallIntegerField(choices=STATUS, default=1, verbose_name='是否有效')

    class Meta:
        verbose_name = '网站'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MessageBoard(models.Model):
    id = models.IntegerField(default=1, primary_key=True,verbose_name='留言id')
    name = models.CharField(max_length=32, verbose_name='留言')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class VisitView(models.Model):
    ip = models.CharField(max_length=32, verbose_name='访问者ip')
    ip_address = models.CharField(max_length=128, verbose_name='访问地址', null=True, blank=True)
    visit_num = models.IntegerField(default=0, verbose_name='访问次数')
    first_visit_time = models.DateTimeField(auto_now_add=True, verbose_name='第一次访问时间')
    last_visit_time = models.DateTimeField(auto_now=True, verbose_name='最后访问时间')

    class Meta:
        verbose_name = '访问统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class FriendsBlog(models.Model):

    STATUS = (
        (0, '无效'),
        (1, '有效')
    )

    name = models.CharField(max_length=64, verbose_name='博客名称')
    address = models.CharField(max_length=64, verbose_name='博客链接')
    status = models.SmallIntegerField(choices=STATUS, default=1, verbose_name='是否有效')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Soul(models.Model):
    """毒鸡汤"""
    title = models.CharField('内容', max_length=512, null=True)
    hits = models.CharField('伤害值', max_length=100, null=True)

    class Meta:
        verbose_name = '毒鸡汤'
        db_table = 'soul'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title