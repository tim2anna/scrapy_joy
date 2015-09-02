#!/usr/bin/python
# -*- coding: utf-8 -*-

import xadmin
from open_insurance.models import Insurance


class InsuranceAdmin(object):
    list_display = ('created', 'insurance_website', 'title', 'amount', 'year_rate', 'duration')
    list_display_links = ('created',)

    list_filter = ['created', 'insurance_website__site']
    actions = None
    aggregate_fields = {"year_rate": "avg", "amount": "sum",}

    refresh_times = (3, 5, 10)

    def _chart_month(self, obj):
        return obj.created.strftime("%m-%d")


xadmin.site.register(Insurance, InsuranceAdmin)