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
import json
import os
from urllib.parse import urljoin

import requests

monitor_url = ""
token = ""

data = {}
for path, dirs, filenames in os.walk("."):
    if not filenames:
        continue

    if path not in [
        "./notice",
        "./notice/snippets",
        "./action",
        "./action/snippets",
        "./rule",
        "./rule/snippets",
    ]:
        continue

    for filename in filenames:
        f = open(os.path.join(path, filename))
        data[f"{path[2:]}/{filename}"] = f.read()
        f.close()

r = requests.post(
    url=urljoin(monitor_url, "/rest/v2/as_code/import_config/"),
    json={
        "bk_biz_id": 2,
        "app": "bk_monitor",
        "configs": data,
    },
    headers={"Authorization": f"Bearer {token}"},
)

print("status_code:", r.status_code)
print(json.dumps(r.json()))
