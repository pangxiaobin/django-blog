from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserInfo(AbstractUser):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('U', '保密'),
    )
    nickname = models.CharField(max_length=32, verbose_name='用户昵称')
    icon = models.ImageField(upload_to='user/icon/', default='', null=True, blank=True, verbose_name='用户头像')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期',)
    sex = models.CharField(max_length=8, choices=SEX, default='U', verbose_name='性别')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username