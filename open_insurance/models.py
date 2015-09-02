#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models.signals import pre_save
from scrapy.contrib.djangoitem import DjangoItem
from dynamic_scraper.models import Scraper, SchedulerRuntime


class InsuranceWebsite(models.Model):
    site = models.CharField(u'平台名称', max_length=20)
    name = models.CharField(u'产品名称', max_length=200)
    area = models.CharField(u'地域', max_length=20, default='', null=True, blank=True)
    category = models.CharField(u'产品类型', max_length=20, default='', null=True, blank=True)
    url = models.URLField(u'爬取链接')
    scraper = models.ForeignKey(Scraper, verbose_name=u'爬虫', blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return self.site + self.name + '[' + str(self.category) + ' ' + str(self.area) + ']'

    class Meta:
        verbose_name = u'保险平台'
        verbose_name_plural = u'保险平台'


class Insurance(models.Model):
    insurance_website = models.ForeignKey(InsuranceWebsite, verbose_name=u'保险平台')
    title = models.CharField(u'借款标题', max_length=200)
    amount = models.FloatField(u'金额(元)', default=0)
    year_rate = models.FloatField(u'年利率%', default=0)
    duration = models.IntegerField(u'期限(天)', default=0)
    url = models.URLField(u'链接地址', blank=True)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(u'录入时间', auto_now_add=True)
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'保险'
        verbose_name_plural = u'保险'


class InsuranceItem(DjangoItem):
    django_model = Insurance


@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, InsuranceWebsite):
        if instance.scraper_runtime:
            instance.scraper_runtime.delete()
    
    if isinstance(instance, Insurance):
        if instance.checker_runtime:
            instance.checker_runtime.delete()
            
pre_delete.connect(pre_delete_handler)