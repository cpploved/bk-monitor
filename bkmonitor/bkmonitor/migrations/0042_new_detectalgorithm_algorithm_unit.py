# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云 - 监控平台 (BlueKing - Monitor) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# Generated by Django 1.11.23 on 2021-12-07 11:11
from core.unit import load_unit

from django.db import migrations


def get_decbytes_to_bytes_suffix_mapping():
    """
    获取decbytes到bytes的单位后缀的映射关系
    :return:
    """
    decbytes_suffix_list = load_unit("decbytes").suffix_list
    bytes_suffix_list = load_unit("bytes").suffix_list

    unit_suffix = dict(zip(decbytes_suffix_list, bytes_suffix_list))
    return unit_suffix


def update_unit_decbytes_to_bytes(apps, *args, **kwargs):
    """
    将原先单位为decbytes的各种策略升级成bytes
    """
    QueryConfigModel = apps.get_model("bkmonitor", "QueryConfigModel")
    AlgorithmModel = apps.get_model("bkmonitor", "AlgorithmModel")
    unit_suffix = get_decbytes_to_bytes_suffix_mapping()
    # 1. 从conf中查找出所有单位为decbytes的，然后将其改为bytes。最后记录对应的策略id
    s_ids = set()
    for query_conf in QueryConfigModel.objects.filter(config__contains={"unit": "decbytes"}):
        s_ids.add(query_conf.strategy_id)
        query_conf.config["unit"] = "bytes"
        query_conf.save()

    # 2. 根据第一步获得的策略id，从检测算法模型中找出对应的数据。依次将unit_prefix进行升级
    for algorithm in AlgorithmModel.objects.filter(strategy_id__in=s_ids):
        algorithm.unit_prefix = unit_suffix.get(algorithm.unit_prefix, "")
        algorithm.save()


class Migration(migrations.Migration):
    dependencies = [
        ("bkmonitor", "0041_auto_20210813_1035"),
    ]

    operations = [
        migrations.RunPython(update_unit_decbytes_to_bytes),
    ]
