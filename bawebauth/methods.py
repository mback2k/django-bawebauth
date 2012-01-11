import logging
from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden
from bawebauth.forms import DeviceForm
from bawebauth.models import User, Device, Usage
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import authenticate

logger = logging.getLogger('django')

def parse_request(request):
    data = {}
    for line in request.readlines():
        if ':' in line:
            line = line.partition(':')
            data[line[0].strip().lower()] = line[2].strip()
    logger.debug(str(data))
    return data

def restore_session(request, session):
    if not request.session or not request.session.session_key == session:
        request.session = SessionStore(session_key=session)
    return request.session

@csrf_exempt
def auth_user(request):
    data = parse_request(request)
    session = request.session
    try:
        User.objects.get(username=data['username'])
    except User.DoesNotExist:
        User.objects.create_user(username=data['username'], email='%s@student.dhbw-mannheim.de' % data['username'], password=data['password'])
    user = authenticate(username=data['username'], password=data['password'])
    if user:
        if user.is_active and user.id > 0:
            session['api_restful_userid'] = user.id
            session.modified = True
            logger.warning('auth_user %s %s %d' % (repr(data), session.session_key, user.id))
            logger.warning('auth_user session %s' % repr(session.keys()))
            return HttpResponse('%s' % session.session_key, mimetype="text/plain")
    session.flush()
    return HttpResponseForbidden('', mimetype="text/plain")

@csrf_exempt
def quit_user(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
    session.flush()
    return HttpResponse('1', mimetype="text/plain")

@csrf_exempt
def create_device(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
    logger.warning('create_device %s %s' % (repr(data), session.session_key))
    logger.warning('create_device session %s' % repr(session.keys()))
    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    device, created = Device.objects.get_or_create(user=user, ident=data['ident'], defaults={'name': data['name']})
    return HttpResponse('%d' % device.id, mimetype="text/plain")

@csrf_exempt
def delete_device(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    device = get_object_or_404(Device, id=int(data['device']), user=user, ident=data['ident'])
    device.delete()
    return HttpResponse('1', mimetype="text/plain")

@csrf_exempt
def push_usage(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    device = get_object_or_404(Device, id=int(data['device']), user=user, ident=data['ident'])
    if 'date' in data:
        usage = Usage.objects.create(user=user, device=device, send=int(data['bytes-send']), received=int(data['bytes-received']), crdate=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'))
    else:
        usage = Usage.objects.create(user=user, device=device, send=int(data['bytes-send']), received=int(data['bytes-received']))
    return HttpResponse('%d' % usage.id, mimetype="text/plain")

@csrf_exempt
def list_usage(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    query = Usage.objects.order_by('-crdate').filter(user=user)
    if 'device' in data:
        device = get_object_or_404(Device, id=int(data['device']), user=user)
        query = query.filter(device=device)
    if 'date-start' in data:
        query = query.filter(crdate__gt=datetime.strptime(data['date-start'], '%Y-%m-%d %H:%M:%S'))
    if 'date-end' in data:
        query = query.filter(crdate__lt=datetime.strptime(data['date-end'], '%Y-%m-%d %H:%M:%S'))
    if 'max-results' in data: 
        query = query[:int(data['max-results'])]
    result = ''
    for usage in query:
        result += "%d\r%s\r%d\r%d\r%s\r\n" % (usage.device.id, usage.device.name, usage.send, usage.received, usage.crdate.strftime('%Y-%m-%d %H:%M:%S'))
    return HttpResponse(result)

@csrf_exempt
def sum_usage(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    query = Usage.objects.order_by('-crdate').filter(user=user)
    if 'device' in data:
        device = get_object_or_404(Device, id=int(data['device']), user=user)
        query = query.filter(device=device)
    if 'date-start' in data:
        query = query.filter(crdate__gt=datetime.strptime(data['date-start'], '%Y-%m-%d %H:%M:%S'))
    if 'date-end' in data:
        query = query.filter(crdate__lt=datetime.strptime(data['date-end'], '%Y-%m-%d %H:%M:%S'))
    if 'max-results' in data: 
        query = query[:int(data['max-results'])]
    sum = {}
    for usage in query:
        if not usage.device.id in sum:
            sum[usage.device.id] = {'send': 0, 'received': 0}
        sum[usage.device.id]['name'] = usage.device.name
        sum[usage.device.id]['send'] += usage.send
        sum[usage.device.id]['received'] += usage.received
    result = ''
    for device_id in sum:
        result += "%d\r%s\r%d\r%d\r\n" % (device_id, sum[device_id]['name'], sum[device_id]['send'], sum[device_id]['received'])
    return HttpResponse(result)
