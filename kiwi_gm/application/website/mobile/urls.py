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
    url(r'^user/search/$', 'ban'),
    url(r'^user/search/$', 'gag'),
)

urlpatterns += patterns('mobile.views.server',
    url(r'^server/sync/$', 'sync'),
)

urlpatterns += patterns('mobile.views.order',
    url(r'^order/by_user/$', 'by_user'),
    url(r'^order/by_order/$', 'by_order'),
    url(r'^order/by_plat/$', 'by_plat'),
    url(r'^order/by_time/$', 'by_time'),
    url(r'^order/rank/$', 'rank'),
)

urlpatterns += patterns('mobile.views.mail',
    url(r'^mail/get/$', 'get_mail'),
    url(r'^mail/send/$', 'send_mail'),
)

urlpatterns += patterns('mobile.views.item',
    url(r'^item/query/$', 'query'),
)

urlpatterns += patterns('mobile.views.send_item',
    url(r'^send/send_item/$', 'send'),
    url(r'^send/delete_item/$', 'delete'),
)

urlpatterns += patterns('mobile.views.action',
    url(r'^action/get/$', 'get_action_info'),
)


# urlpatterns += patterns('mobile.views.recharge',
#     url(r'^recharge/search_recharge/$', 'search_recharge'),
# )

# urlpatterns += patterns('mobile.views.sendmessage',
#     url(r'^sendmessage/send/$', 'sendmessage'),
# )

# urlpatterns += patterns('mobile.views.element',
#     url(r'^element/search_element/$', 'search_element'),
#     url(r'^element/delete_element/$', 'delete_element'),
# )

# urlpatterns += patterns('mobile.views.feedback',
#     url(r'^feedback/response/$', 'response'),
#     url(r'^feedback/send_email/$', 'send_email'),
#     url(r'^feedback/$', 'get_feedback_info'),
# )

# urlpatterns += patterns('mobile.views.welfare',
#     url(r'^welfare/send_welfare/$', 'send_welfare'),
# )
