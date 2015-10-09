#!/usr/bin/python
# -*- coding: utf-8 -*-

import xadmin
from open_loan.models import Loan, LoanCategory, LoanScraper, LoanWebsite


class LoanAdmin(object):
    list_display = ('created', 'loan_scraper', 'title', 'amount', 'year_rate', 'duration')
    list_display_links = ('created',)

    list_filter = ['created', 'site', 'category2']
    actions = None
    aggregate_fields = {"year_rate": "avg", "amount": "sum",}

    refresh_times = (3, 5, 10)

xadmin.site.register(Loan, LoanAdmin)


class LoanCategoryAdmin(object):
    exclude = ('fullname', )

xadmin.site.register(LoanCategory, LoanCategoryAdmin)


class LoanScraperAdmin(object):
    list_display = ('name', 'url', 'site', 'category1', 'category2')

xadmin.site.register(LoanScraper, LoanScraperAdmin)


class LoanWebsiteAdmin(object):
    list_filter = ['area']

xadmin.site.register(LoanWebsite, LoanWebsiteAdmin)