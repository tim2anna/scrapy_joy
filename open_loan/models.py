#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models.signals import pre_save
from scrapy.contrib.djangoitem import DjangoItem
from dynamic_scraper.models import Scraper, SchedulerRuntime


class LoanCategory(models.Model):
    name = models.CharField(u'分类名称', max_length=200)
    parent = models.ForeignKey(
        'self', verbose_name=u'上级分类', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)
    fullname = models.CharField(u'分类全称', max_length=200)

    def __unicode__(self):
        return self.fullname

    class Meta:
        verbose_name = u'标的分类'
        verbose_name_plural = u'标的分类'


@receiver(pre_save, sender=LoanCategory, dispatch_uid='open_loan.loan_category')
def loan_category_set(sender, **kwargs):
    """ 设置全称 """
    instance = kwargs.get('instance')
    if instance.parent:
        instance.fullname = instance.parent.fullname + '-' + instance.name
    else:
        instance.fullname = instance.name


class LoanWebsite(models.Model):
    name = models.CharField(u'平台名称', max_length=20)
    area = models.CharField(u'地域', max_length=20, default='')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'网贷平台'
        verbose_name_plural = u'网贷平台'


class LoanScraper(models.Model):
    name = models.CharField(u'名称', max_length=200)
    url = models.URLField(u'爬取链接')
    weight = models.FloatField(u'权重', default=1)
    site = models.ForeignKey(LoanWebsite, verbose_name=u'网贷平台')
    category1 = models.ForeignKey(LoanCategory, verbose_name=u'一级分类', related_name='category1_scraper')
    category2 = models.ForeignKey(LoanCategory, verbose_name=u'二级分类', related_name='category2_scraper')

    scraper = models.ForeignKey(Scraper, verbose_name=u'爬虫', blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'标的爬虫'
        verbose_name_plural = u'标的爬虫'


class Loan(models.Model):
    TERM_UNIT_CHOICES = (
        ('day', u'天'),
        ('month', u'月'),
    )

    loan_scraper = models.ForeignKey(LoanScraper, verbose_name=u'标的爬虫')
    title = models.CharField(u'借款标题', max_length=200)
    amount = models.FloatField(u'金额(元)', default=0)
    year_rate = models.FloatField(u'年利率%', default=0)

    duration = models.IntegerField(u'期限(天)', default=0)
    term = models.IntegerField(u'期限', default=0)
    term_unit = models.CharField(u'期限单位', max_length=10, choices=TERM_UNIT_CHOICES)

    url = models.URLField(u'链接地址', blank=True)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(u'录入时间', auto_now_add=True)

    site = models.ForeignKey(LoanWebsite, verbose_name=u'网贷平台')
    category1 = models.ForeignKey(LoanCategory, verbose_name=u'一级分类', related_name='category1_loans')
    category2 = models.ForeignKey(LoanCategory, verbose_name=u'二级分类', related_name='category2_loans')
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'标的'
        verbose_name_plural = u'标的'


class LoanItem(DjangoItem):
    django_model = Loan


@receiver(pre_save, sender=Loan, dispatch_uid='open_loan.loan')
def loan_push_product(sender, **kwargs):
    instance = kwargs.get('instance')

    if instance.term_unit not in ['day', 'month']:
        exec(instance.loan_scraper.scraper.comments)

    if instance.term_unit == 'day':
        instance.duration = instance.term
    elif instance.term_unit == 'month':
        instance.duration = int(instance.term)*30

    if instance.loan_scraper:
        instance.site = instance.loan_scraper.site
        instance.category1 = instance.loan_scraper.category1
        instance.category2 = instance.loan_scraper.category2


class StaDayData(models.Model):
    """ 聚合天数据 """
    TERM_UNIT_CHOICES = (
        ('day', u'天'),
        ('month', u'个月'),
    )

    sta_date = models.DateField(u'日期')
    site = models.ForeignKey(LoanWebsite, verbose_name=u'网贷平台')
    sta_cnt = models.IntegerField(u'样本数量')
    category1 = models.ForeignKey(LoanCategory, verbose_name=u'一级分类', related_name='category1_sta_day_data', null=True)
    category2 = models.ForeignKey(LoanCategory, verbose_name=u'二级分类', related_name='category2_sta_day_data', null=True)
    term = models.IntegerField(u'期限', default=0)
    term_unit = models.CharField(u'期限单位', max_length=10, choices=TERM_UNIT_CHOICES)
    rate = models.FloatField(u'利率', null=True, blank=True)


class SubscribeEmail(models.Model):
    """ 订阅邮箱 """
    email = models.EmailField(u'邮箱')
    created = models.DateTimeField(u'订阅时间', auto_now_add=True)


class Legend(models.Model):
    """ 图例 """
    name = models.CharField(u'名称', max_length=20)
    is_show = models.BooleanField(u'是否显示', default=False)
    sort_num = models.IntegerField(u'排序号', default=1)
    category = models.CharField(u'分类', max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = u'图例'
        verbose_name_plural = u'图例'