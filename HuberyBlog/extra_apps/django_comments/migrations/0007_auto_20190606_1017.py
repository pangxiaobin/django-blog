# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-06-06 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments', '0006_auto_20190603_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name="user's email address"),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="user's name"),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_url',
            field=models.URLField(blank=True, null=True, verbose_name="user's URL"),
        ),
    ]
