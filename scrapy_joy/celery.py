#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Celery for Django

从celery3.1开始，django中使用celery，不再需要使用djcelery库
"""

# from __future__ import absolute_import
#
# import os, sys, django
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy_joy.settings")
# django.setup()
#
# from celery import Celery, platforms
# from django.conf import settings
#
# app = Celery('scrapy_joy')
#
# platforms.C_FORCE_ROOT = True
#
# # Using a string here means the worker will not have to pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)