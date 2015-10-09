#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Celery for Django

从celery3.1开始，django中使用celery，不再需要使用djcelery库
"""

from __future__ import absolute_import

import os
import django
from celery import Celery
from django.conf import settings


# 为Celery程序设置Django的默认配置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy_joy.settings")
django.setup()

app = Celery('scrapy_joy')

# Using a string here means the worker will not have to pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)