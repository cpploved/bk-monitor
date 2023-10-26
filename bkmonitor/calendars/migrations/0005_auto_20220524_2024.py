# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2022-05-24 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0004_check_and_fix_repeat_every'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarmodel',
            name='deep_color',
            field=models.CharField(default='#3A84FF', max_length=7, verbose_name='日历深色底色'),
        ),
        migrations.AlterField(
            model_name='calendarmodel',
            name='light_color',
            field=models.CharField(default='#E1ECFF', max_length=7, verbose_name='日历浅色底色'),
        ),
    ]
