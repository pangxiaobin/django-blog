from django.db import models

# Create your models here.


class Hot(models.Model):
    STATUS = (
        (0, '无效'),
        (1, '有效')
    )
    hot_name = models.CharField('热榜源', max_length=256, null=True)
    content = models.TextField('内容', null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.SmallIntegerField(choices=STATUS, default=1, verbose_name='是否有效')
    sorted = models.SmallIntegerField('排序', default=0)

    class Meta:
        ordering = ['-sorted']