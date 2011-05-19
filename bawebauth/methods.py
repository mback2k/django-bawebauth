import logging
from datetime import datetime
from django.http import HttpResponse
from bawebauth.forms import DeviceForm
from bawebauth.models import User, Device, Usage
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore

def parse_request(request):
    data = {}
    for line in request.readlines():
        if ':' in line:
            line = line.partition(':')
            data[line[0].strip().lower()] = line[2].strip()
    logging.info(str(data))
    return data

def restore_session(request, session):
    if not request.session:
        request.session = SessionStore(session_key=session)
    return request.session

@csrf_exempt
def auth_user(request):
    data = parse_request(request)
    user, created = User.objects.get_or_create(username=data['username'], email='%s@student.dhbw-mannheim.de' % data['username'])
    user.set_password(data['password'])
    user.save()
    request.session['api_restful_userid'] = user.id
    return HttpResponse('%s' % request.session.session_key, mimetype="text/plain")

@csrf_exempt
def create_device(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
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
        usage, created = Usage.objects.create(user=user, device=device, send=int(data['bytes-send']), received=int(data['bytes-received']), crdate=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'))
    else:
        usage, created = Usage.objects.create(user=user, device=device, send=int(data['bytes-send']), received=int(data['bytes-received']))
    return HttpResponse('%d' % usage.id, mimetype="text/plain")

@csrf_exempt
def list_usage(request):
    data = parse_request(request)
    session = restore_session(request, data['user'])
    user = get_object_or_404(User, id=int(session['api_restful_userid']))
    query = Usage.objects.filter(user=user)
    if 'device' in data:
        device = get_object_or_404(Device, id=int(data['device']), user=user)
        query = query.filter(device=device)
    if 'max-results' in data: 
        query = query[:int(data['max-results'])]
    if 'date-start' in data:
        query = query.filter(crdate__gt=datetime.strptime(data['date-start'], '%Y-%m-%d %H:%M:%S'))
    if 'date-end' in data:
        query = query.filter(crdate__lt=datetime.strptime(data['date-end'], '%Y-%m-%d %H:%M:%S'))
    result = ''
    for usage in query:
        result += "%d\r%s\r%d\r%d\r%s\r\n" % (device.id, device.name, usage.send, usage.received, usage.crdate.strftime('%Y-%m-%d %H:%M:%S'))
    return HttpResponse(result)
