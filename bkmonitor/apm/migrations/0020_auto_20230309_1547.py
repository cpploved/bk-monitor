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
# Generated by Django 1.11.23 on 2023-03-09 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apm", "0019_datalink_influxdb_cluster_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="topoinstance",
            name="component_instance_category",
            field=models.CharField(max_length=255, null=True, verbose_name="组件实例分类(service类型下为空)"),
        ),
        migrations.AddField(
            model_name="topoinstance",
            name="component_instance_predicate_value",
            field=models.CharField(max_length=255, null=True, verbose_name="组件实例类型(service类型下为空)"),
        ),
        migrations.AddField(
            model_name="topoinstance",
            name="instance_topo_kind",
            field=models.CharField(default=None, max_length=255, verbose_name="实例类型"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="toporelation",
            name="to_topo_key_category",
            field=models.CharField(default=None, max_length=255, verbose_name="目标节点分类"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="toporelation",
            name="to_topo_key_kind",
            field=models.CharField(default=None, max_length=255, verbose_name="目标节点类型"),
            preserve_default=False,
        ),
    ]
