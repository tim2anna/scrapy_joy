#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy_joy.settings")
django.setup()

from datetime import date, timedelta
from celery.task import task
from dynamic_scraper.utils.task_utils import TaskUtils

from django.db import transaction
from django.db.models import Sum, Avg
from django.core import mail
from django.template import Context, loader

from scrapy_joy import settings
from open_loan.models import LoanScraper, Loan, StaDayData, LoanCategory, LoanWebsite, SubscribeEmail


@task()
def run_spiders():
    t = TaskUtils()
    t.run_spiders(LoanScraper, 'scraper', 'scraper_runtime', 'loan_spider')


@task()
def run_checkers():
    t = TaskUtils()
    t.run_checkers(Loan, 'loan_website__scraper', 'checker_runtime', 'loan_checker')


@task()
@transaction.atomic
def run_sta_day_data(sta_day=(date.today() - timedelta(days=1))):
    # 删除该日期的统计数据，避免重复数据
    StaDayData.objects.filter(sta_date=sta_day).delete()

    site_dict = dict([(i.name, i) for i in LoanWebsite.objects.all()])
    cat_dict = dict([(i.fullname, i) for i in LoanCategory.objects.all()])

    # 查询该日期的所有原始标的信息，并归类
    loans = Loan.objects.filter(created__range=(sta_day, sta_day+timedelta(days=1)))
    cat1_dict, cat2_dict = {}, {}

    for loan in loans:
        if loan.category1.fullname not in cat1_dict:
            cat1_dict[loan.category1.fullname] = {}
        if loan.category2.fullname not in cat2_dict:
            cat2_dict[loan.category2.fullname] = {}

        if u'活期' in loan.category1.fullname:
            term = 1
        elif loan.duration < 90:
            term = 1
        elif loan.duration < 180:
            term = 3
        elif loan.duration < 270:
            term = 6
        elif loan.duration < 360:
            term = 9
        elif loan.duration < 540:
            term = 12
        elif loan.duration < 720:
            term = 18
        elif loan.duration < 1080:
            term = 24
        else:
            term = 36

        if term not in cat1_dict[loan.category1.fullname]:
            cat1_dict[loan.category1.fullname][term] = {}
        if term not in cat2_dict[loan.category2.fullname]:
            cat2_dict[loan.category2.fullname][term] = {}

        if loan.site.name not in cat1_dict[loan.category1.fullname][term]:
            cat1_dict[loan.category1.fullname][term][loan.site.name] = []
        if loan.site.name not in cat2_dict[loan.category2.fullname][term]:
            cat2_dict[loan.category2.fullname][term][loan.site.name] = []

        cat1_dict[loan.category1.fullname][term][loan.site.name].append(loan.year_rate)
        cat2_dict[loan.category2.fullname][term][loan.site.name].append(loan.year_rate)

    for cat1 in cat1_dict:
        for term in cat1_dict[cat1]:
            for site in cat1_dict[cat1][term]:
                item = cat1_dict[cat1][term][site]
                data = StaDayData(
                    sta_date=sta_day,
                    site=site_dict.get(site),
                    category1=cat_dict.get(cat1),
                    term=term,
                    term_unit=StaDayData.TERM_UNIT_CHOICES[1][0],
                    rate=sum(item)/len(item),
                    sta_cnt=len(item),
                )
                data.save()

    for cat2 in cat2_dict:
        for term in cat2_dict[cat2]:
            for site in cat2_dict[cat2][term]:
                item = cat2_dict[cat2][term][site]
                data = StaDayData(
                    sta_date=sta_day,
                    site=site_dict.get(site),
                    category2=cat_dict.get(cat2),
                    term=term,
                    term_unit=StaDayData.TERM_UNIT_CHOICES[1][0],
                    rate=sum(item)/len(item),
                    sta_cnt=len(item),
                )
                data.save()


@task()
def send_week_email(mail_list=[], today=date.today()):
    """ 周指数邮件 """
    if not mail_list:
        mail_list = [obj.email for obj in SubscribeEmail.objects.all()]

    subject = u'【Kaisa利率】周指数'

    last_week_start_date = today + timedelta(-7 - today.weekday())  # 上周星期一
    last_week_end_date = today + timedelta(-today.weekday())  # 上周星期一
    last_week_loans = Loan.objects.filter(created__range=(last_week_start_date, last_week_end_date))
    last_week_loan_cnt = last_week_loans.count()
    last_week_loan_rate = last_week_loans.aggregate(avg=Avg('year_rate'))['avg'] or 0
    last_week_loan_amount = last_week_loans.aggregate(sum=Sum('amount'))['sum'] or 0
    host_name = settings.HOST_NAME

    email_template_name = 'week_email.html'
    t = loader.get_template(email_template_name)
    html_content = t.render(Context(locals()))

    conn = mail.get_connection()
    conn.open()
    msg_list = []
    for to in mail_list:
        msg = mail.EmailMultiAlternatives(subject, html_content, settings.DEFAULT_FROM_EMAIL, [to, ])
        msg.attach_alternative(html_content, "text/html")
        msg_list.append(msg)
    conn.send_messages(msg_list)
    conn.close()


@task()
def send_month_email(mail_list=[], today=date.today()):
    """ 周指数邮件 """
    if not mail_list:
        mail_list = [obj.email for obj in SubscribeEmail.objects.all()]

    subject = u'【Kaisa利率】月指数'

    if today.month <= 1:
        last_month_start_date = date(day=1, month=12, year=today.year-1)
    else:
        last_month_start_date = date(day=1, month=today.month-1, year=today.year)
    last_month_end_date = date(day=1, month=today.month, year=today.year) - timedelta(days=1)  # 上月最后一天
    last_month_loans = Loan.objects.filter(created__range=(last_month_start_date, last_month_end_date))
    last_month_loan_cnt = last_month_loans.count()
    last_month_loan_rate = last_month_loans.aggregate(avg=Avg('year_rate'))['avg'] or 0
    last_month_loan_amount = last_month_loans.aggregate(sum=Sum('amount'))['sum'] or 0
    host_name = settings.HOST_NAME

    email_template_name = 'month_email.html'
    t = loader.get_template(email_template_name)
    html_content = t.render(Context(locals()))

    conn = mail.get_connection()
    conn.open()
    msg_list = []
    for to in mail_list:
        msg = mail.EmailMultiAlternatives(subject, html_content, settings.DEFAULT_FROM_EMAIL, [to, ])
        msg.attach_alternative(html_content, "text/html")
        msg_list.append(msg)
    conn.send_messages(msg_list)
    conn.close()


if __name__ == "__main__":
    run_sta_day_data()