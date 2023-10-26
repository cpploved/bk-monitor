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
# Generated by Django 1.11.23 on 2022-10-08 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apm", "0015_merge_20221008_1621"),
    ]

    operations = [
        migrations.CreateModel(
            name="QpsConfig",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("bk_biz_id", models.IntegerField(verbose_name='业务id')),
                ("app_name", models.CharField(max_length=128, verbose_name="应用名称")),
                ("config_level", models.CharField(max_length=50, verbose_name="配置级别")),
                ("config_key", models.CharField(max_length=255, verbose_name="配置key")),
                ("qps", models.IntegerField(default=500, verbose_name="QPS")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
