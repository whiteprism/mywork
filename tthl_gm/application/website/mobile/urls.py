# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.conf import settings
from mobile.views import *
urlpatterns = patterns('',
    # Example:
    # (r'^something/', include('application.foo.urls')),
)

urlpatterns += patterns('mobile.views.index',
    url(r'^$', 'index'),
    url(r'^model/$', 'model'),
)

urlpatterns += patterns('mobile.views.user',
    url(r'^user/search/$', 'search'),
    url(r'^user/ban/$', 'ban'),
    url(r'^user/gag/$', 'gag'),
)

urlpatterns += patterns('mobile.views.action',
    url(r'^action/search/$', 'search_action'),
)

urlpatterns += patterns('mobile.views.server',
    url(r'^server/search/$', 'search_server'),
    url(r'^server/search_notime/$', 'search_server_notime'),
)

urlpatterns += patterns('mobile.views.recharge',
    url(r'^recharge/search_recharge/$', 'search_recharge'),
)

urlpatterns += patterns('mobile.views.sendmessage',
    url(r'^sendmessage/send/$', 'sendmessage'),
)

urlpatterns += patterns('mobile.views.element',
    url(r'^element/search_element/$', 'search_element'),
    url(r'^element/delete_element/$', 'delete_element'),
)

urlpatterns += patterns('mobile.views.welfare',
    url(r'^welfare/send_welfare/$', 'send_welfare'),
)

urlpatterns += patterns('mobile.views.order',
    url(r'^order/search_order/$', 'search_order'),
    url(r'^order/add_order/$', 'add_order'),
    url(r'^order/fake_order/$', 'fake_order'),
)

urlpatterns += patterns('mobile.views.feedback',
    url(r'^feedback/response/$', 'response'),
    url(r'^feedback/send_email/$', 'send_email'),
    url(r'^feedback/$', 'get_feedback_info'),
    url(r'^check_feedback/(\d{1,})/$', 'check_feedback'),
)

urlpatterns += patterns('mobile.views.activity',
    url(r'^activity/add_activity/$', 'add_activity'),
    url(r'^activity/get_activity/$', 'get_activity'),
)
# urlpatterns += patterns('mobile.views.user',
#     url(r'^user/search/$', 'search'),
#     url(r'^action/search/$', 'search_action'),
#     url(r'^server/search/$', 'search_server'),
#     url(r'^server/search_notime/$', 'search_server_notime'),
#     url(r'^recharge/search_recharge/$', 'search_recharge'),
#     url(r'^sendmessage/send/$', 'sendmessage'),
#     url(r'^element/search_element/$', 'search_element'),
#     url(r'^element/delete_element/$', 'delete_element'),
#     url(r'^welfare/send_welfare/$', 'send_welfare'),
#     url(r'^order/search_order/$', 'search_order'),
#     url(r'^order/fake_order/$', 'fake_order'),
#     url(r'^user/ban/$', 'ban'),
#     url(r'^user/gag/$', 'gag'),
# )

