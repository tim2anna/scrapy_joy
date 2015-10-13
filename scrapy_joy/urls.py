from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

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

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
