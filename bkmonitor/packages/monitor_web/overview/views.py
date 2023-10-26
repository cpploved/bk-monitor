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

from bkmonitor.iam import ActionEnum
from bkmonitor.iam.drf import BusinessActionPermission
from core.drf_resource import resource
from core.drf_resource.viewsets import ResourceRoute, ResourceViewSet


class PermissionMixin:
    def get_permissions(self):
        return [BusinessActionPermission([ActionEnum.VIEW_BUSINESS])]


class AlarmRankViewSet(PermissionMixin, ResourceViewSet):
    """
    告警类型排行
    """

    resource_routes = [
        ResourceRoute("GET", resource.overview.alarm_rank),
    ]


class AlarmCountInfoViewSet(PermissionMixin, ResourceViewSet):
    """
    告警数量信息
    """

    resource_routes = [
        ResourceRoute("GET", resource.overview.alarm_count_info),
    ]


class MonitorInfoViewSet(PermissionMixin, ResourceViewSet):
    """
    业务监控状态总览
    """

    resource_routes = [
        ResourceRoute("GET", resource.overview.monitor_info),
    ]
