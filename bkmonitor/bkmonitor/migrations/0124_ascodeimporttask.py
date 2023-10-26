# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2022-12-20 03:36
from __future__ import unicode_literals

from django.db import migrations, models

import bkmonitor.models.as_code


class Migration(migrations.Migration):

    dependencies = [
        ('bkmonitor', '0123_auto_20221220_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsCodeImportTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bk_biz_id', models.IntegerField(verbose_name='业务ID')),
                ('params', models.JSONField(default=dict, verbose_name='导入参数')),
                ('file', models.FileField(upload_to=bkmonitor.models.as_code._get_file_path, verbose_name='配置压缩包')),
                ('result', models.TextField(null=True, verbose_name='导入结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': 'AS 代码导入历史',
                'verbose_name_plural': 'AS 代码导入历史',
                'db_table': 'as_code_import_history',
                'ordering': ['-create_time'],
            },
        ),
    ]
