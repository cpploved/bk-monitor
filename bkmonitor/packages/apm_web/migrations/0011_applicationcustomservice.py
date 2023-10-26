# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云 - 监控平台 (BlueKing - Monitor) available.
Copyright (C) 2017-2022 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# Generated by Django 1.11.23 on 2022-06-27 13:47
from __future__ import unicode_literals

from django.db import migrations, models

import bkmonitor.utils.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("apm_web", "0010_auto_20220625_1143"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplicationCustomService",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_enabled", models.BooleanField(default=True, verbose_name="是否启用")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="是否删除")),
                ("create_user", models.CharField(blank=True, default="", max_length=32, verbose_name="创建人")),
                ("create_time", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("update_user", models.CharField(blank=True, default="", max_length=32, verbose_name="最后修改人")),
                ("update_time", models.DateTimeField(auto_now=True, verbose_name="最后修改时间")),
                ("bk_biz_id", models.IntegerField(verbose_name="业务id")),
                ("app_name", models.CharField(max_length=50, verbose_name="应用名称")),
                ("name", models.CharField(max_length=128, verbose_name="名称")),
                ("type", models.CharField(choices=[("http", "http")], max_length=32, verbose_name="服务类型")),
                (
                    "match_type",
                    models.CharField(
                        choices=[("auto", "自动匹配"), ("manual", "手动匹配")], max_length=32, verbose_name="匹配类型"
                    ),
                ),
                ("rule", bkmonitor.utils.db.fields.JsonField(verbose_name="匹配规则")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
