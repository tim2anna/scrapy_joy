#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from open_insurance.models import InsuranceWebsite, Insurance


class InsuranceWebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'name', 'url_', 'scraper')
    list_display_links = ('name',)
    
    def url_(self, instance):
        return '<a href="%s" target="_blank">%s</a>' % (instance.url, instance.url)
    url_.allow_tags = True


class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'year_rate', 'duration', 'insurance_website', 'url_', 'created')
    list_display_links = ('title',)
    raw_id_fields = ('checker_runtime',)
    
    def url_(self, instance):
        return '<a href="%s" target="_blank">%s</a>' % (instance.url, instance.url)
    url_.allow_tags = True

admin.site.register(InsuranceWebsite, InsuranceWebsiteAdmin)
admin.site.register(Insurance, InsuranceAdmin)