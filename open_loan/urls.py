from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'open_loan.views.index', name='index'),
    url(r'^week_trends/$', 'open_loan.views.week_trends', name='week_trends'),
    url(r'^month_trends/$', 'open_loan.views.month_trends', name='month_trends'),
    url(r'^loans/$', 'open_loan.views.loans', name='loans'),
    url(r'^subscribe/$', 'open_loan.views.subscribe', name='subscribe'),
)
