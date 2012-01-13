# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from bawebauth.decorators import cache_property
from django.utils.translation import ugettext_lazy as _

class Device(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(_('name'), max_length=100)
    ident = models.CharField(_('ident'), max_length=40)
    crdate = models.DateTimeField(_('date created'), auto_now_add=True)
    tstamp = models.DateTimeField(_('date edited'), auto_now=True)
    
    def __unicode__(self):
        return self.name

    @cache_property
    def usages(self):
        return self.usage_set.order_by('crdate')
        
    @cache_property
    def last_usage(self):
        return self.usage_set.latest('crdate')

class Usage(models.Model):
    user = models.ForeignKey(User)
    device = models.ForeignKey(Device)
    send = models.IntegerField(_('bytes send'))
    received = models.IntegerField(_('bytes received'))
    crdate = models.DateTimeField(_('date created'), auto_now_add=True)
    
    def __unicode__(self):
        return u'%s %s+ %s-' % (self.crdate, self.send, self.received)
