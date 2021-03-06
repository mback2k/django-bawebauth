# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils import timezone
from .models import User, Device, Usage
import datetime
import logging
import re

logger = logging.getLogger('django')

def parse_request(request):
    data = {}
    for line in request.readlines():
        line = line.decode('utf-8').partition(':')
        if line[1] == ':':
            data[line[0].strip().lower()] = line[2].strip()
    logger.debug(str(data))
    return data

def restore_session(request, session):
    if not request.session or not request.session.session_key == session:
        request.session = SessionStore(session_key=session)
    return request.session

def create_password(user):
    current_site = Site.objects.get_current()
    website_link = 'https://%s%s' % (current_site.domain, reverse('bawebauth:show_home'))
    random_password = get_random_string()
    user.set_password(random_password)
    user.save()
    user.email_user('BaWebAuth - Login using your new password',
                    'You logged in using BaWebAuth for the very first time.\n' \
                    'A new account has been setup to allow you to measure the total traffic of your devices:\n\n' \
                    'Username: %s\n' \
                    'Password: %s\n\n' \
                    'You can login at %s and manage your devices.' % (user.username, random_password, website_link))
    return user

def create_user(username):
    if re.search(r's\d{6}', username):
        mail = '%s@student.dhbw-mannheim.de' % username
    else:
        mail = '%s@dhbw-mannheim.de' % username
    user = User.objects.create_user(username=username, email=mail)
    return create_password(user)

@csrf_exempt
def auth_user(request):
    data = parse_request(request)
    if not 'username' in data:
        return HttpResponseBadRequest('', content_type='text/plain')

    session = request.session
    try:
        user = User.objects.get(username=data['username'].lower())
    except User.DoesNotExist:
        user = create_user(data['username'].lower())

    if user and user.is_active:
        session['api_restful_userid'] = user.id
        session.modified = True
        session.save()
        return HttpResponse('%s' % session.session_key, content_type='text/plain')

    session.flush()

    return HttpResponseForbidden('', content_type='text/plain')

@csrf_exempt
def quit_user(request):
    data = parse_request(request)
    if not 'user' in data:
        return HttpResponseBadRequest('', content_type='text/plain')

    session = restore_session(request, data['user'])
    session.flush()

    return HttpResponse('1', content_type='text/plain')

@csrf_exempt
def create_device(request):
    data = parse_request(request)
    if not 'user' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'name' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'ident' in data:
        return HttpResponseBadRequest('', content_type='text/plain')

    session = restore_session(request, data['user'])
    if not 'api_restful_userid' in session:
        return HttpResponseForbidden('', content_type='text/plain')

    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    device, created = Device.objects.get_or_create(user=user, ident=data['ident'], defaults={'name': data['name']})
    if created:
        current_site = Site.objects.get_current()
        website_link = 'https://%s%s' % (current_site.domain, reverse('bawebauth:show_dashboard'))
        user.email_user('BaWebAuth - Please activate your new device',
                        'A new device named "%s" has been used with your account.\n\n' \
                        'Please go to %s and activate your devices.' % (device.name, website_link))

    return HttpResponse('%d' % device.id, content_type='text/plain')

@csrf_exempt
def delete_device(request):
    data = parse_request(request)
    if not 'user' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'ident' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'device' in data:
        return HttpResponseBadRequest('', content_type='text/plain')

    session = restore_session(request, data['user'])
    if not 'api_restful_userid' in session:
        return HttpResponseForbidden('', content_type='text/plain')

    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    device = get_object_or_404(Device, id=int(data['device']), user=user, ident=data['ident'])
    device.delete()

    return HttpResponse('1', content_type='text/plain')

@csrf_exempt
def push_usage(request):
    data = parse_request(request)
    if not 'user' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'ident' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'device' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'bytes-send' in data:
        return HttpResponseBadRequest('', content_type='text/plain')
    if not 'bytes-received' in data:
        return HttpResponseBadRequest('', content_type='text/plain')

    session = restore_session(request, data['user'])
    if not 'api_restful_userid' in session:
        return HttpResponseForbidden('', content_type='text/plain')

    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    device = get_object_or_404(Device, id=int(data['device']), user=user, ident=data['ident'])
    if not device.active or not device.enabled:
        return HttpResponse('0', content_type='text/plain')

    if 'date' in data:
        crdate = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        usage = Usage.objects.create(device=device, send=int(data['bytes-send']), received=int(data['bytes-received']), crdate=crdate)
    else:
        usage = Usage.objects.create(device=device, send=int(data['bytes-send']), received=int(data['bytes-received']))

    return HttpResponse('%d' % usage.id, content_type='text/plain')

@csrf_exempt
def list_usage(request):
    data = parse_request(request)
    if not 'user' in data:
        return HttpResponseBadRequest('', content_type='text/plain')

    session = restore_session(request, data['user'])
    if not 'api_restful_userid' in session:
        return HttpResponseForbidden('', content_type='text/plain')

    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    query = Usage.objects.order_by('-crdate').filter(device__user=user).filter(device__enabled=True)
    if 'device' in data:
        device = get_object_or_404(Device, id=int(data['device']), user=user)
        query = query.filter(device=device)
    if 'date-start' in data:
        date_start = datetime.datetime.strptime(data['date-start'], '%Y-%m-%d %H:%M:%S')
        query = query.filter(crdate__gt=date_start)
    if 'date-end' in data:
        date_end = datetime.datetime.strptime(data['date-end'], '%Y-%m-%d %H:%M:%S')
        query = query.filter(crdate__lt=date_end)
    if 'max-results' in data:
        query = query[:int(data['max-results'])]

    result = ''
    for usage in query:
        result += "%d\r%s\r%d\r%d\r%s\r\n" % (usage.device.id, usage.device.name, usage.send, usage.received, usage.crdate.strftime('%Y-%m-%d %H:%M:%S'))

    return HttpResponse(result)

@csrf_exempt
def device_usage(request):
    data = parse_request(request)
    if not 'user' in data:
        return HttpResponseBadRequest('', content_type='text/plain')

    session = restore_session(request, data['user'])
    if not 'api_restful_userid' in session:
        return HttpResponseForbidden('', content_type='text/plain')

    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    query = Device.objects.order_by('name').filter(user=user).filter(enabled=True)
    if 'device' in data:
        query = query.filter(id=int(data['device']))
    if 'date-start' in data:
        date_start = datetime.datetime.strptime(data['date-start'], '%Y-%m-%d %H:%M:%S')
        query = query.filter(usage__crdate__gt=date_start)
    if 'date-end' in data:
        date_end = datetime.datetime.strptime(data['date-end'], '%Y-%m-%d %H:%M:%S')
        query = query.filter(usage__crdate__lt=date_end)
    query = query.annotate(join_send=Sum('usage__send'), join_received=Sum('usage__received'))
    if 'max-results' in data:
        query = query[:int(data['max-results'])]

    result = ''
    for device in query:
        result += "%d\r%s\r%d\r%d\r\n" % (device.id, device.name, device.join_send, device.join_received)

    return HttpResponse(result)


def api_usages_etag(request, format='json'):
    if not format in ['xml', 'json', 'yaml']:
        return None
    return 'id-%d' % Usage.objects.latest('crdate').id

def api_usages_last_modified(request, format='json'):
    if not format in ['xml', 'json', 'yaml']:
        return None
    return Usage.objects.latest('crdate').crdate

@condition(etag_func=api_usages_etag, last_modified_func=api_usages_last_modified)
def api_usages(request, format='json'):
    if not format in ['xml', 'json', 'yaml']:
        return HttpResponseBadRequest()
    usages = Usage.objects.filter(crdate__gt=timezone.now()-datetime.timedelta(days=30)).order_by('crdate')
    output = serializers.serialize(format, usages, fields=('send', 'received', 'crdate'))
    return HttpResponse(output, content_type='application/%s' % format)

@login_required
def api_device_usages(request, device_id, format='json'):
    device = get_object_or_404(Device, user=request.user, id=device_id)
    if not format in ['xml', 'json', 'yaml']:
        return HttpResponseBadRequest()
    content = serializers.serialize(format, device.usages)
    return HttpResponse(content, content_type='application/%s' % format)
