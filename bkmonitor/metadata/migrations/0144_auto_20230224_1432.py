# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2023-02-24 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0143_add_apm_label_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='influxdbhostinfo',
            name='grpc_port',
            field=models.IntegerField(default=8089, verbose_name='GRPC端口'),
        ),
        migrations.AddField(
            model_name='influxdbhostinfo',
            name='protocol',
            field=models.CharField(default='http', max_length=16, verbose_name='协议'),
        ),
        migrations.AddField(
            model_name='influxdbhostinfo',
            name='read_rate_limit',
            field=models.FloatField(default=0, verbose_name='读取速率'),
        ),
    ]
