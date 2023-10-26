# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2022-04-15 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("metadata", "0114_auto_20220330_2008"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="downsampledcontinuousqueries",
            options={"verbose_name": "降精度策略配置", "verbose_name_plural": "降精度策略配置"},
        ),
        migrations.AlterModelOptions(
            name="downsampleddatabase",
            options={"verbose_name": "降精度数据库配置", "verbose_name_plural": "降精度数据库配置"},
        ),
        migrations.AlterModelOptions(
            name="downsampledretentionpolicies",
            options={"verbose_name": "降精度rp配置", "verbose_name_plural": "降精度rp配置"},
        ),
        migrations.AlterField(
            model_name="logcollectorinfo",
            name="bk_data_id",
            field=models.BigIntegerField(db_index=True, verbose_name="数据源ID"),
        ),
        migrations.AlterField(
            model_name="podmonitorinfo",
            name="bk_data_id",
            field=models.BigIntegerField(db_index=True, verbose_name="数据源ID"),
        ),
        migrations.AlterField(
            model_name="servicemonitorinfo",
            name="bk_data_id",
            field=models.BigIntegerField(db_index=True, verbose_name="数据源ID"),
        ),
    ]
