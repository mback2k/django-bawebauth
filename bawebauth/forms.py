# -*- coding: utf-8 -*-
from django import forms
from bawebauth.models import Device

class DeviceForm(forms.ModelForm):
    name = forms.CharField(required=True,
        label='Name', help_text='Type in a client name.')

    class Meta:
        model = Device
        fields = ['name']
