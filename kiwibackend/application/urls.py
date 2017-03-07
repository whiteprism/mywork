# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


handler500 = "website.mobile.views.error.page_500"
handler404 = "website.mobile.views.error.page_404"

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('mobile.urls')),
)
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
