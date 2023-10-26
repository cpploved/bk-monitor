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

from django.conf.urls import include, url
from fta_web.views import home

app_name = "fta_web"

urlpatterns = [
    url(r"^$", home),
    url(r"^plugin/", include("fta_web.event_plugin.urls")),
    url(r"^alert/", include("fta_web.alert.urls")),
    url(r"^action/", include("fta_web.action.urls")),
    url(r"^assign/", include("fta_web.assign.urls")),
    url(r"^home/", include("fta_web.home.urls")),
]
