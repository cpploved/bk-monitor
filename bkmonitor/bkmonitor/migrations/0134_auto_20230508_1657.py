# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2023-05-08 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkmonitor', '0133_merge_20230419_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportitems',
            name='channels',
            field=models.JSONField(default=dict, verbose_name='订阅渠道'),
        ),
        migrations.AddField(
            model_name='reportitems',
            name='is_link_enabled',
            field=models.BooleanField(default=True, verbose_name='是否发送链接'),
        ),
    ]
