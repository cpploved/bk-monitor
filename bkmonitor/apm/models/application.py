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
from django.db import models
from django.db.transaction import atomic
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from apm.constants import DATABASE_CONNECTION_NAME
from bkmonitor.utils.cipher import transform_data_id_to_token
from bkmonitor.utils.model_manager import AbstractRecordModel

MetricDataSource = None
TraceDataSource = None


class ApmApplication(AbstractRecordModel):
    bk_biz_id = models.IntegerField("业务id")
    app_name = models.CharField("应用名称", max_length=50)
    app_alias = models.CharField("应用别名", max_length=128)
    description = models.CharField("应用描述", max_length=255)
    is_enabled = models.BooleanField("是否启用", default=True)

    class Meta:
        unique_together = ("app_name", "bk_biz_id")

    def start(self):
        for datasource in [MetricDataSource, TraceDataSource]:
            datasource.start(bk_biz_id=self.bk_biz_id, app_name=self.app_name)
        self.is_enabled = True
        self.save()

    def stop(self):
        for datasource in [MetricDataSource, TraceDataSource]:
            datasource.stop(bk_biz_id=self.bk_biz_id, app_name=self.app_name)

        self.is_enabled = False
        self.save()

    @classmethod
    def get_application(cls, bk_biz_id, app_name):
        try:
            return ApmApplication.objects.get(bk_biz_id=bk_biz_id, app_name=app_name)
        except ApmApplication.DoesNotExist:
            raise ValueError(_("应用不存在"))

    @classmethod
    def apply_datasource(cls, bk_biz_id, app_name, es_storage_config):
        application = cls.objects.filter(bk_biz_id=bk_biz_id, app_name=app_name).first()
        if not application:
            raise ValueError(_("应用({}) 不存在").format(app_name))

        # 默认创建和更新trace数据源和指标数据源
        for datasource in [TraceDataSource, MetricDataSource]:
            datasource.apply_datasource(bk_biz_id=bk_biz_id, app_name=app_name, **es_storage_config)

        return {
            "metric_config": application.metric_datasource.to_json(),
            "trace_config": application.trace_datasource.to_json(),
        }

    @classmethod
    @atomic(using=DATABASE_CONNECTION_NAME)
    def create_application(cls, bk_biz_id, app_name, app_alias, description, es_storage_config):
        if cls.objects.filter(bk_biz_id=bk_biz_id, app_name=app_name).exists():
            raise ValueError(_("应用名称(app_name) {} 在该业务({})已经存在").format(app_name, bk_biz_id))
        # step1: 创建应用
        application = cls.objects.create(
            bk_biz_id=bk_biz_id,
            app_name=app_name,
            app_alias=app_alias,
            description=description,
        )

        # step2: 创建结果表
        datasource_info = cls.apply_datasource(bk_biz_id, app_name, es_storage_config)

        # step3: 创建虚拟指标
        from apm.task.tasks import create_virtual_metric

        create_virtual_metric.delay(bk_biz_id, app_name)

        return {
            "bk_biz_id": bk_biz_id,
            "app_name": app_name,
            "application_id": application.id,
            "datasource_info": datasource_info,
        }

    @cached_property
    def trace_datasource(self):
        return TraceDataSource.objects.filter(bk_biz_id=self.bk_biz_id, app_name=self.app_name).first()

    @cached_property
    def metric_datasource(self):
        return MetricDataSource.objects.filter(bk_biz_id=self.bk_biz_id, app_name=self.app_name).first()

    def get_bk_data_token(self):
        if not self.metric_datasource:
            return ""
        params = {
            "trace_data_id": self.trace_datasource.bk_data_id,
            "metric_data_id": self.metric_datasource.bk_data_id,
            "bk_biz_id": self.bk_biz_id,
            "app_name": self.app_name,
        }
        return transform_data_id_to_token(**params)


class RootEndpoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    bk_biz_id = models.IntegerField("业务id")
    app_name = models.CharField("应用名称", max_length=50)
    endpoint_name = models.CharField("接口", max_length=2048)
    service_name = models.CharField("服务名称", max_length=2048)
    category_id = models.CharField("分类名称", max_length=128)
    created_at = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("更新时间", blank=True, null=True, auto_now=True, db_index=True)


class Endpoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    bk_biz_id = models.IntegerField("业务id")
    app_name = models.CharField("应用名称", max_length=50)
    endpoint_name = models.CharField("接口", max_length=2048)
    service_name = models.CharField("服务名称", max_length=2048)
    category_id = models.CharField("分类名称", max_length=128)
    category_kind_key = models.CharField("分类类型key", max_length=255)
    category_kind_value = models.CharField("分类类型值", max_length=255)
    span_kind = models.IntegerField("跟踪类型", default=0)
    extra_data = models.TextField(null=True, verbose_name="额外数据")
    created_at = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("更新时间", blank=True, null=True, auto_now=True, db_index=True)


class EbpfApplicationConfig(models.Model):
    bk_biz_id = models.IntegerField(verbose_name="业务id")
    application_id = models.IntegerField("应用Id")

    class Meta:
        verbose_name = "ebpf应用配置"
