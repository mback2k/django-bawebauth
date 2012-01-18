# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('bawebauth.views',
    (r'^$', 'show_home'),
    (r'^dashboard/$', 'show_dashboard'),
    (r'^dashboard/device/(?P<device_id>\d+)/$', 'show_device'),
    (r'^dashboard/device/(?P<device_id>\d+)/edit/$', 'edit_device'),
    (r'^dashboard/device/(?P<device_id>\d+)/delete/$', 'delete_device'),
    (r'^dashboard/device/(?P<device_id>\d+)/delete/ask/$', 'delete_device_ask'),
)

urlpatterns += patterns('bawebauth.methods',
    (r'^api/restful/user/auth/$', 'auth_user'),
    (r'^api/restful/user/quit/$', 'quit_user'),
    (r'^api/restful/device/create/$', 'create_device'),
    (r'^api/restful/device/delete/$', 'delete_device'),
    (r'^api/restful/usage/push/$', 'push_usage'),
    (r'^api/restful/usage/list/$', 'list_usage'),
    (r'^api/restful/usage/sum/$', 'device_usage'),
)

urlpatterns += patterns('bawebauth.methods',
    (r'^api/restful/device/(?P<device_id>\d+)/usages\.(?P<format>\w+)$', 'api_device_usages'),
)
