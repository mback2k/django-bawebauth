# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from .forms import DeviceForm
from .models import Device, Usage

def show_home(request):
    return render_to_response('show_home.html', context_instance=RequestContext(request))

@login_required
def show_dashboard(request):
    devices = Device.objects.all().filter(user=request.user).order_by('name')
    
    template_values = {
        'devices': devices,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def show_device(request, device_id):
    devices = Device.objects.all().filter(user=request.user).order_by('name')
    device = get_object_or_404(Device, user=request.user, id=device_id)

    template_values = {
        'devices': devices,
        'device': device,
    }
    
    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def edit_device(request, device_id):
    devices = Device.objects.all().filter(user=request.user).order_by('name')
    device = get_object_or_404(Device, user=request.user, id=device_id)
    edit_form = DeviceForm(instance=device, data=request.POST if request.method == 'POST' else None)

    if edit_form.is_valid():
        device = edit_form.save(commit=False)
        device.user = request.user
        device.save()
        return HttpResponseRedirect(reverse('bawebauth:show_device', kwargs={'device_id': device.id}))
    
    template_values = {
        'devices': devices,
        'device': device,
        'device_edit_form': edit_form,
    }
    
    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def switch_device(request, device_id):
    devices = Device.objects.all().filter(user=request.user).order_by('name')
    device = get_object_or_404(Device, user=request.user, id=device_id)
    device.enabled = not(device.enabled)
    device.active = True
    device.save()
    
    messages.success(request, 'Switched device "%s" %s!' % (device, 'on' if device.enabled else 'off'))
    
    return HttpResponseRedirect(reverse('bawebauth:show_device', kwargs={'device_id': device.id}))

@login_required
def delete_device(request, device_id):
    devices = Device.objects.all().filter(user=request.user).order_by('name')
    device = get_object_or_404(Device, user=request.user, id=device_id)
    device.delete()
    
    messages.success(request, 'Deleted device "%s" from your Dashboard!' % device)
    
    template_values = {
        'devices': devices,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def delete_device_ask(request, device_id):
    devices = Device.objects.all().filter(user=request.user).order_by('name')
    device = get_object_or_404(Device, user=request.user, id=device_id)

    button = '<a class="ym-button ym-delete float-right" href="%s" title="Yes">Yes</a>' % reverse('bawebauth:delete_device', kwargs={'device_id': device.id})     
    messages.warning(request, '%sDo you want to delete device "%s"?' % (button, device))
    
    template_values = {
        'devices': devices,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))
