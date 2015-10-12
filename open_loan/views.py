#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import date, timedelta, datetime
from collections import OrderedDict

from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from django.db.models import Sum, Avg
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

from open_loan.models import Loan, LoanWebsite, StaDayData, SubscribeEmail
from open_loan.helpers import get_sta_time_by_week, get_sta_time_by_month
from open_loan.forms import SubscribeForm
from open_loan.tasks import send_week_email


def index(request):
    today = date.today()

    website_cnt = LoanWebsite.objects.count()
    loan_cnt = Loan.objects.count()

    last_week_start_date = today + timedelta(-7 - today.weekday())  # 上周星期一
    last_week_end_date = today + timedelta(-today.weekday())  # 上周星期天

    this_week_loans = Loan.objects.filter(created__gt=last_week_end_date)
    last_week_loans = Loan.objects.filter(created__range=(last_week_start_date, last_week_end_date))

    this_week_loan_cnt = this_week_loans.count()
    last_week_loan_cnt = last_week_loans.count()

    this_week_loan_rate = this_week_loans.aggregate(avg=Avg('year_rate'))['avg'] or 0
    last_week_loan_rate = last_week_loans.aggregate(avg=Avg('year_rate'))['avg'] or 0

    this_week_loan_amount = this_week_loans.aggregate(sum=Sum('amount'))['sum'] or 0
    last_week_loan_amount = last_week_loans.aggregate(sum=Sum('amount'))['sum'] or 0

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


def week_trends(request):
    """ 周指数 """
    current_menu = 'week_trends'
    today = date.today()

    start_date = request.GET.get('start_date')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = today + timedelta(-7*10 - today.weekday())  # 前10周的星期一

    end_date = request.GET.get('end_date')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = today + timedelta(-1 - today.weekday())  # 上周的星期天

    q = StaDayData.objects.filter(
        category1=None, sta_date__range=(start_date, end_date)
    ).order_by('category2', 'term', '-sta_date')

    # 明细数据
    week_dict, series_dict = OrderedDict(), OrderedDict()
    category2_options, term_options = set(), set()
    for obj in q:
        week = u'%s第%s周' % (obj.sta_date.year, int(obj.sta_date.strftime('%W'))+1)
        if week not in week_dict:
            week_dict[week] = OrderedDict()
        cat2 = obj.category2.fullname
        if cat2 not in week_dict[week]:
            week_dict[week][cat2] = OrderedDict()
        term = str(obj.term) + obj.get_term_unit_display()
        if term not in week_dict[week][cat2]:
            week_dict[week][cat2][term] = []
        week_dict[week][cat2][term].append(
            {'rate': obj.rate, 'sta_cnt': obj.sta_cnt}
        )

        if cat2 not in series_dict:
            series_dict[cat2] = OrderedDict()
        if term not in series_dict[cat2]:
            series_dict[cat2][term] = OrderedDict()
        if week not in series_dict[cat2][term]:
            series_dict[cat2][term][week] = []
        series_dict[cat2][term][week].append(
            {'rate': obj.rate, 'sta_cnt': obj.sta_cnt}
        )

        category2_options.add(obj.category2)
        term_options.add(str(obj.term) + obj.get_term_unit_display())

    # 汇总表格数据
    table_data = []
    for week, cat_dict in week_dict.items():
        for cat, term_dict in cat_dict.items():
            for term, item_list in term_dict.items():
                table_data.append((
                    week,
                    '~'.join([i.strftime('%Y-%m-%d')for i in get_sta_time_by_week(week)]),
                    cat,
                    term,
                    sum([item['rate']*item['sta_cnt'] for item in item_list]) / sum([item['sta_cnt'] for item in item_list])
                ))

    # 折线图数据
    chart_data = []
    for cat, term_dict in series_dict.items():
        for term, week_dict in term_dict.items():
            data = []
            for week, item_list in week_dict.items():
                data.append([
                    week,
                    sum([item['rate']*item['sta_cnt'] for item in item_list]) / sum([item['sta_cnt'] for item in item_list])
                ])
            chart_data.append({
                'name': cat + '-' + term,
                'type': 'line',
                'showAllSymbol': True,
                'data': data
            })

    return render_to_response('week_trends.html', locals(), context_instance=RequestContext(request))


def month_trends(request):
    """ 月指数 """
    current_menu = 'month_trends'
    today = date.today()

    start_date = request.GET.get('start_date')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = date.today() - timedelta(days=7)
        # 前6个月的第一天
        if today.month <= 6:
            start_date = date(day=1, month=6+today.month, year=today.year-1)
        else:
            start_date = date(day=1, month=today.month-6, year=today.year)

    end_date = request.GET.get('end_date')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = date(day=1, month=today.month, year=today.year) - timedelta(days=1)  # 上月最后一天

    q = StaDayData.objects.filter(
        category1=None, sta_date__range=(start_date, end_date)
    ).order_by('-sta_date', 'category2', 'term')

    # 明细数据
    month_dict, series_dict = OrderedDict(), OrderedDict()
    for obj in q:
        month = u'%s年%s月' % (obj.sta_date.year, obj.sta_date.month)
        if month not in month_dict:
            month_dict[month] = OrderedDict()
        cat2 = obj.category2.fullname
        if cat2 not in month_dict[month]:
            month_dict[month][cat2] = OrderedDict()
        term = str(obj.term) + obj.get_term_unit_display()
        if term not in month_dict[month][cat2]:
            month_dict[month][cat2][term] = []
        month_dict[month][cat2][term].append(
            {'rate': obj.rate, 'sta_cnt': obj.sta_cnt}
        )

        if cat2 not in series_dict:
            series_dict[cat2] = OrderedDict()
        if term not in series_dict[cat2]:
            series_dict[cat2][term] = OrderedDict()
        if month not in series_dict[cat2][term]:
            series_dict[cat2][term][month] = []
        series_dict[cat2][term][month].append(
            {'rate': obj.rate, 'sta_cnt': obj.sta_cnt}
        )

    # 汇总表格数据
    table_data = []
    for month, cat_dict in month_dict.items():
        for cat, term_dict in cat_dict.items():
            for term, item_list in term_dict.items():
                table_data.append((
                    month,
                    '~'.join([i.strftime('%Y-%m-%d')for i in get_sta_time_by_month(month)]),
                    cat,
                    term,
                    sum([item['rate']*item['sta_cnt'] for item in item_list]) / sum([item['sta_cnt'] for item in item_list])
                ))

    # 折线图数据
    chart_data = []
    for cat, term_dict in series_dict.items():
        for term, month_dict in term_dict.items():
            data = []
            for month, item_list in month_dict.items():
                data.append([
                    month,
                    sum([item['rate']*item['sta_cnt'] for item in item_list]) / sum([item['sta_cnt'] for item in item_list])
                ])
            chart_data.append({
                'name': cat + '-' + term,
                'type': 'line',
                'showAllSymbol': True,
                'data': data
            })

    return render_to_response('month_trends.html', locals(), context_instance=RequestContext(request))


def loans(request):
    """ 原始数据 """
    current_menu = 'loans'

    start_date = request.GET.get('start_date')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = date.today() - timedelta(days=7)

    end_date = request.GET.get('end_date')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = date.today() + timedelta(days=1)

    site_id = [int(i) for i in request.REQUEST.getlist('site_id')]

    page = int(request.GET.get('page', 1))

    q = Loan.objects.filter(created__range=(start_date, end_date))
    if site_id:
        q = q.filter(site_id__in=site_id)

    q = q.order_by('-created')
    paginator = Paginator(q, 15)
    try:
        curr_page = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        curr_page = paginator.page(1)
    if page >= 5:
        page_range = paginator.page_range[page - 5:page + 5]
    else:
        page_range = paginator.page_range[0:int(page) + 5]

    return_url = '?start_date=%s&end_date=%s&%s' % (start_date, end_date, '&'.join(['site_id='+str(i)for i in site_id]))
    site_list = LoanWebsite.objects.all()

    return render_to_response('loans.html', locals(), context_instance=RequestContext(request))


@csrf_protect
def subscribe(request):
    """ 订阅 """
    if request.method == 'POST':
        form = SubscribeForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            q = SubscribeEmail.objects.filter(email=email)
            send_week_email.delay([email, ])
            if q:
                return HttpResponse(json.dumps({'status': 0, 'info': u'已订阅'}), content_type='application/json')
            else:
                SubscribeEmail.objects.create(email=email)
                return HttpResponse(json.dumps({'status': 1, 'info': u'订阅成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 0, 'info': u'邮箱格式错误'}), content_type='application/json')



