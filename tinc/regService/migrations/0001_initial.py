# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('netname', models.CharField(default='tinc', max_length=100, verbose_name='netname')),
                ('net', models.GenericIPAddressField(default='10.0.0.0', verbose_name='net')),
                ('netmask', models.PositiveSmallIntegerField(default=16, verbose_name='netmask')),
                ('secret', models.CharField(max_length=32, verbose_name='secret')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(default='', max_length=100, verbose_name='hostname')),
                ('public_IP', models.GenericIPAddressField(verbose_name='public IP')),
                ('config_IP', models.GenericIPAddressField(verbose_name='config IP')),
                ('private_IP', models.GenericIPAddressField(verbose_name='private IP')),
                ('private_netmask', models.PositiveSmallIntegerField(default=32, verbose_name='netmask')),
                ('pub_key', models.TextField(verbose_name='pub Key')),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regService.Network')),
            ],
        ),
    ]
