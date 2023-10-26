# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2022-04-19 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bkmonitor", "0089_merge_20220418_2135"),
    ]

    operations = [
        migrations.AddField(
            model_name="strategymodel",
            name="invalid_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", ""),
                    ("invalid_metric", "监控指标不存在"),
                    ("invalid_target", "监控目标全部失效"),
                    ("invalid_related_strategy", "关联的策略已失效"),
                    ("deleted_related_strategy", "关联的策略已删除"),
                ],
                default="",
                max_length=32,
                verbose_name="失效类型",
            ),
        ),
    ]
