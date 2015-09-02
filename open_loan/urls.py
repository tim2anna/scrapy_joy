from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'open_loan.views.index', name='index'),
)
