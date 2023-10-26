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
from datetime import datetime

import dateutil.parser
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def test_translate_timestamp_since():
    start_time = '2022-01-01T00:00:00Z'
    # 获得UTC时间
    start_at = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    start_at_utc = timezone.make_aware(start_at, timezone.utc)
    # 转换为当前时区的时间
    current_timezone = timezone.get_current_timezone()
    start_at_current_timezone = start_at_utc.astimezone(current_timezone)
    start_at_current_timezone_naive = timezone.make_naive(start_at_current_timezone)
    assert start_at_current_timezone_naive == datetime(2022, 1, 1, 8, 0)


def test_from_iso_format():
    start_time = "2022-01-01T00:00:00+00:00"
    start_time_obj = dateutil.parser.isoparse(start_time)
    # 转换为当前时区的时间
    current_timezone = timezone.get_current_timezone()
    start_at_current_timezone = start_time_obj.astimezone(current_timezone)
    start_at_current_timezone_naive = timezone.make_naive(start_at_current_timezone)
    assert start_at_current_timezone_naive == datetime(2022, 1, 1, 8, 0)


def test_parse_datetime():
    start_time = "2022-01-01T00:00:00+00:00"
    start_time_obj = parse_datetime(start_time)
    # 转换为当前时区的时间
    current_timezone = timezone.get_current_timezone()
    start_at_current_timezone = start_time_obj.astimezone(current_timezone)
    start_at_current_timezone_naive = timezone.make_naive(start_at_current_timezone)
    assert start_at_current_timezone_naive == datetime(2022, 1, 1, 8, 0)
