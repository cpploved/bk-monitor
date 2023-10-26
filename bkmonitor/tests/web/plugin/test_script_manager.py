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

import copy
import os

import pytest
import yaml
from django.conf import settings
from django.db.models.query import QuerySet

from monitor_web.models.plugin import (
    CollectorPluginConfig,
    CollectorPluginInfo,
    CollectorPluginMeta,
    OperatorSystemManager,
    PluginVersionHistory,
)
from monitor_web.plugin.manager import PluginManagerFactory

from .test_base_manager import CONFIG_DATA, CURRENT_VERSION_DATA, INFO_DATA, PLUGIN_DATA


@pytest.fixture
def update_plugin_manager(mocker):
    create_params = copy.deepcopy(PLUGIN_DATA)
    create_params.pop("scripts")
    create_params.pop("plugin_display_name")
    plugin = CollectorPluginMeta(**create_params)
    config = CollectorPluginConfig(**CONFIG_DATA)
    info = CollectorPluginInfo(**INFO_DATA)
    CURRENT_VERSION_DATA.update({"plugin": plugin, "config": config, "info": info})
    version = PluginVersionHistory(**CURRENT_VERSION_DATA)
    mocker.patch.object(PluginVersionHistory.objects, "filter", return_value=QuerySet())
    mocker.patch.object(QuerySet, "last", return_value=version)
    plugin_manager = PluginManagerFactory.get_manager(plugin, "admin")
    return plugin_manager


class TestScriptManager(object):
    def test_get_collector_json(self, mocker, update_plugin_manager):
        plugin_params = {
            "meta.yaml": yaml.dump({"scripts": {"windows": {"type": "bat", "filename": "test_plugin.bat"}}})
        }
        mocker.patch(
            "os.path.join",
            side_effect=[
                "test_plugin.bat",
                os.path.join(settings.BASE_DIR, "tests/web/plugin/test_data/test_plugin.bat"),
            ],
        )
        assert update_plugin_manager.get_collector_json(plugin_params) == {
            "windows": {
                "filename": "test_plugin.bat",
                "script_content_base64": "QGVjaG8gb2ZmDQplY2hvIGhvc3QgMTE=",
                "type": "bat",
            }
        }

    def test_get_debug_config_context(self, update_plugin_manager, mocker):
        params = {
            "collector": {"period": "10"},
            "plugin": {"param_pos_cmd": "11", "params_env": "22", "params_opt_cmd": "33"},
        }
        get_version_mock = mocker.patch.object(
            CollectorPluginMeta, "get_version", return_value=update_plugin_manager.version
        )
        assert update_plugin_manager.get_debug_config_context(1, 1, params) == {
            "bkmonitorbeat_debug.yaml": {"period": "10"},
            "env.yaml": {"cmd_args": "param_pos_cmd 11 params_opt_cmd 33 ", "params_env": "22"},
        }
        get_version_mock.assert_called_once_with(1, 1)

    def test_fetch_collector_file(self, update_plugin_manager, mocker):
        os_type_list_mock = mocker.patch.object(
            OperatorSystemManager, "os_type_list", return_value=["linux", "windows", "aix"]
        )
        result = update_plugin_manager.fetch_collector_file()
        result["windows"][0]["file_content"] = result["windows"][0]["file_content"].replace("\r\n", "\n")
        assert result == {"windows": [{"file_content": "@echo off\necho 111", "file_name": "test_plugin.bat"}]}
        os_type_list_mock.assert_called_once()
