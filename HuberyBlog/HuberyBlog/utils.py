#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 20-4-30 下午4:42
# @Author  : Hubery
# @File    : utils.py
# @Software: PyCharm
import os


def check_file_path(file_path):

    if isinstance(file_path, list):
        for file in file_path:
            if not os.path.exists(file):
                os.makedirs(file)
    else:
        if not os.path.exists(file_path):
            os.makedirs(file_path)