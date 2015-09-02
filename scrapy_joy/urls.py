from django.conf.urls import patterns, include, url

import xadmin
xadmin.autodiscover()

# from xadmin.plugins import xversion
# xversion.registe_models()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
    url(r'^', include('open_loan.urls')),
)
