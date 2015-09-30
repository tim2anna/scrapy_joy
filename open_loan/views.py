#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
from collections import OrderedDict

from django.template import RequestContext
from django.shortcuts import render_to_response

from open_loan.models import Loan, LoanWebsite, StaDayData
from open_loan.helpers import get_sta_time_by_week, get_sta_time_by_month


def index(request):
    # start_date = request.GET.get('start_date')
    # if start_date:
    #     start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    # else:
    #     start_date = date.today() - timedelta(days=7)
    #
    # end_date = request.GET.get('end_date')
    # if end_date:
    #     end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    # else:
    #     end_date = date.today()
    #
    # for day in range((end_date-start_date).days):
    #     print day
    #
    # sites = LoanWebsite.objects.all()
    #
    # sites = dict([(site.id, {'loans': [], 'site': site, 'category': site.category}) for site in sites])
    #
    # loans = Loan.objects.filter(created__range=(start_date, end_date))
    # for loan in loans:
    #     sites[loan.loan_website_id]['loans'].append(loan)
    #
    # sites = sites.values()

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
    ).order_by('-sta_date', 'category2')

    # 明细数据
    week_dict, series_dict = OrderedDict(), OrderedDict()
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
    ).order_by('-sta_date', 'category2')

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
        end_date = date.today()

    q = Loan.objects.all()

    return render_to_response('loans.html', locals(), context_instance=RequestContext(request))



