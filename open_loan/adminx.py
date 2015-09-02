#!/usr/bin/python
# -*- coding: utf-8 -*-

import xadmin
from open_loan.models import Loan


class LoanAdmin(object):
    list_display = ('created', 'loan_website', 'title', 'amount', 'year_rate', 'duration')
    list_display_links = ('created',)

    list_filter = ['created', 'loan_website__site']
    actions = None
    aggregate_fields = {"year_rate": "avg", "amount": "sum",}

    refresh_times = (3, 5, 10)
    # data_charts = {
    #     "per_day": {
    #         'title': u"日趋势图(年利率)",
    #         "x-field": "_chart_month",
    #         "y-field": ("year_rate", ),
    #         "order": ('created',),
    #         "option": {
    #             "series": {"lines": {'show': True, }},
    #             "xaxis": {"aggregate": "avg", "mode": "categories"},
    #         },
    #     },
    # }

    def _chart_month(self,obj):
        return obj.created.strftime("%m-%d")


xadmin.site.register(Loan, LoanAdmin)