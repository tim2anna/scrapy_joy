#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta


def get_sta_time_by_week(week=u'2015第1周'):
    """ 根据周次计算这周开始日期和结束日期 """
    year = int(week[:4])
    week = int(week[-2]) if len(week) == 7 else int(week[-3:-1])
    day = datetime.strptime("%s-01-01" % year, '%Y-%m-%d') + timedelta(days=(week-1)*7)
    start_day = day + timedelta(- day.weekday())
    end_day = day + timedelta(6 - day.weekday())
    return start_day.date(), end_day.date()


def get_sta_time_by_month(month=u'2015年12月'):
    """ 根据月份计算这月开始日期和结束日期 """
    year = int(month[:4])
    month = int(month[-2]) if len(month) == 7 else int(month[-3:-1])
    start_day = date.today().replace(year=year, month=month, day=1)
    if month == 12:
        end_day = date.today().replace(year=year+1, month=1, day=1) - timedelta(days=1)
    else:
        end_day = date.today().replace(year=year, month=month+1, day=1) - timedelta(days=1)
    return start_day, end_day


if __name__ == '__main__':
    print get_sta_time_by_month()