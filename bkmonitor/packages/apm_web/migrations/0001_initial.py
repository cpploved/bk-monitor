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
# Generated by Django 1.11.23 on 2022-01-20 10:02
from __future__ import unicode_literals

from django.db import migrations, models

import bkmonitor.utils.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ApmMetaConfig",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("config_level", models.CharField(max_length=128, verbose_name="配置级别")),
                ("level_key", models.CharField(max_length=30, verbose_name="配置目标key")),
                ("config_key", models.CharField(max_length=255, verbose_name="config key")),
                ("config_value", bkmonitor.utils.db.fields.JsonField(verbose_name="配置信息")),
            ],
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                ("is_enabled", models.BooleanField(default=True, verbose_name="是否启用")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="是否删除")),
                ("create_user", models.CharField(blank=True, default="", max_length=32, verbose_name="创建人")),
                ("create_time", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("update_user", models.CharField(blank=True, default="", max_length=32, verbose_name="最后修改人")),
                ("update_time", models.DateTimeField(auto_now=True, verbose_name="最后修改时间")),
                ("application_id", models.IntegerField(primary_key=True, serialize=False, verbose_name="应用Id")),
                ("bk_biz_id", models.IntegerField(verbose_name="业务id")),
                ("app_name", models.CharField(max_length=50, verbose_name="应用名称")),
                ("app_alias", models.CharField(max_length=128, verbose_name="应用别名")),
                ("description", models.CharField(max_length=255, verbose_name="应用描述")),
                ("metric_result_table_id", models.CharField(default="", max_length=255, verbose_name="指标结果表")),
                ("trace_result_table_id", models.CharField(default="", max_length=255, verbose_name="Trace结果表")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ApplicationRelationInfo",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("application_id", models.IntegerField(verbose_name="应用Id")),
                ("relation_key", models.CharField(max_length=255, verbose_name="关联Key")),
                ("relation_value", models.CharField(max_length=255, verbose_name="关联值")),
            ],
        ),
    ]
