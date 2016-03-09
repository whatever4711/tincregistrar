# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-09 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regService', '0003_auto_20160309_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='subnet',
        ),
        migrations.AddField(
            model_name='node',
            name='private_SN',
            field=models.PositiveSmallIntegerField(default=32, verbose_name='private Subnet'),
        ),
    ]