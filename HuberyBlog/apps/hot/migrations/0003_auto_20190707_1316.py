# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-07 13:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hot', '0002_auto_20190707_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hot',
            options={'ordering': ['-sorted']},
        ),
    ]
