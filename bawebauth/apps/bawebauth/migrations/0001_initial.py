# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import bawebauth.apps.bawebauth.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('ident', models.CharField(max_length=40, verbose_name='ident')),
                ('crdate', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('tstamp', models.DateTimeField(auto_now=True, verbose_name='date edited')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('enabled', models.BooleanField(default=False, verbose_name='enabled')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('send', bawebauth.apps.bawebauth.fields.PositiveBigIntegerField(verbose_name='bytes send')),
                ('received', bawebauth.apps.bawebauth.fields.PositiveBigIntegerField(verbose_name='bytes received')),
                ('crdate', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('device', models.ForeignKey(to='bawebauth.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
