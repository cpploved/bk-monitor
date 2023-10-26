# Generated by Django 3.2.15 on 2023-07-17 06:41

from django.db import migrations, models

import bkmonitor.utils.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apm_web', '0014_auto_20220718_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='TraceComparison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_user', models.CharField(blank=True, default='', max_length=32, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_user', models.CharField(blank=True, default='', max_length=32, verbose_name='最后修改人')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('bk_biz_id', models.IntegerField(verbose_name='业务id')),
                ('app_name', models.CharField(max_length=50, verbose_name='应用名称')),
                ('trace_id', models.CharField(max_length=32, verbose_name='trace ID')),
                ('name', models.CharField(max_length=16, verbose_name='参照名称')),
                ('spans', bkmonitor.utils.db.fields.JsonField(verbose_name='span list')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
