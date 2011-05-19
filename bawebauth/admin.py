from django.contrib import admin
from bawebauth.models import Device, Usage

class DeviceAdmin(admin.ModelAdmin):
    fields = ('user', 'name', 'ident')
    list_display = ('user', 'name', 'crdate', 'tstamp')
    ordering = ('crdate',)

class UsageAdmin(admin.ModelAdmin):
    fields = ('device', 'send', 'received')
    list_display = ('device', 'send', 'received', 'crdate')
    ordering = ('crdate',)

admin.site.register(Device, DeviceAdmin)
admin.site.register(Usage, UsageAdmin)
