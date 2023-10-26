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


import logging

from django.db import models

from bkmonitor.utils.db import JsonField

logger = logging.getLogger("apm")


class SubscriptionConfig(models.Model):
    """
    APM订阅ID记录
    """

    # 0 is global default config
    bk_biz_id = models.IntegerField("业务id")

    # "" is global default config
    app_name = models.CharField("应用名称", max_length=128)

    subscription_id = models.IntegerField("节点管理订阅ID", default=0)
    config = JsonField(verbose_name="订阅配置")
