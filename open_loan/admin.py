#!/usr/bin/python
# -*- coding: utf-8 -*-

# from django.contrib import admin
# from open_loan.models import LoanWebsite, Loan
#
#
# class LoanWebsiteAdmin(admin.ModelAdmin):
#     list_display = ('id', 'site', 'name', 'url_', 'scraper')
#     list_display_links = ('name',)
#
#     def url_(self, instance):
#         return '<a href="%s" target="_blank">%s</a>' % (instance.url, instance.url)
#     url_.allow_tags = True
#
#
# class LoanAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'amount', 'year_rate', 'duration', 'loan_website', 'url_', 'created')
#     list_display_links = ('title',)
#     raw_id_fields = ('checker_runtime',)
#
#     def url_(self, instance):
#         return '<a href="%s" target="_blank">%s</a>' % (instance.url, instance.url)
#     url_.allow_tags = True
#
# admin.site.register(LoanWebsite, LoanWebsiteAdmin)
# admin.site.register(Loan, LoanAdmin)