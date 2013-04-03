# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views, methods

urlpatterns = patterns('',
    url(r'^$', views.show_home, name='show_home'),
    url(r'^dashboard/$', views.show_dashboard, name='show_dashboard'),
    url(r'^dashboard/device/(?P<device_id>\d+)/$', views.show_device, name='show_device'),
    url(r'^dashboard/device/(?P<device_id>\d+)/edit/$', views.edit_device, name='edit_device'),
    url(r'^dashboard/device/(?P<device_id>\d+)/switch/$', views.switch_device, name='switch_device'),
    url(r'^dashboard/device/(?P<device_id>\d+)/delete/$', views.delete_device, name='delete_device'),
    url(r'^dashboard/device/(?P<device_id>\d+)/delete/ask/$', views.delete_device_ask, name='delete_device_ask'),
)

urlpatterns += patterns('',
    url(r'^api/restful/user/auth/$', methods.auth_user, name='auth_user'),
    url(r'^api/restful/user/quit/$', methods.quit_user, name='quit_user'),
    url(r'^api/restful/device/create/$', methods.create_device, name='create_device'),
    url(r'^api/restful/device/delete/$', methods.delete_device, name='delete_device'),
    url(r'^api/restful/usage/push/$', methods.push_usage, name='push_usage'),
    url(r'^api/restful/usage/list/$', methods.list_usage, name='list_usage'),
    url(r'^api/restful/usage/sum/$', methods.device_usage, name='device_usage'),
)

urlpatterns += patterns('',
    url(r'^api/restful/device/(?P<device_id>\d+)/usages\.(?P<format>\w+)$', methods.api_device_usages, name='api_device_usages'),
)
