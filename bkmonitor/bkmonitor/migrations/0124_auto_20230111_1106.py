# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2023-01-11 03:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkmonitor', '0123_auto_20221220_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithmmodel',
            name='type',
            field=models.CharField(
                choices=[
                    ('Threshold', '静态阈值算法'),
                    ('SimpleRingRatio', '简易环比算法'),
                    ('AdvancedRingRatio', '高级环比算法'),
                    ('SimpleYearRound', '简易同比算法'),
                    ('AdvancedYearRound', '高级同比算法'),
                    ('PartialNodes', '部分节点数算法'),
                    ('OsRestart', '主机重启算法'),
                    ('ProcPort', '进程端口算法'),
                    ('PingUnreachable', 'Ping不可达算法'),
                    ('YearRoundAmplitude', '同比振幅算法'),
                    ('YearRoundRange', '同比区间算法'),
                    ('RingRatioAmplitude', '环比振幅算法'),
                    ('IntelligentDetect', '智能异常检测算法'),
                    ('TimeSeriesForecasting', '时序预测算法'),
                    ('AbnormalCluster', '离群检测算法'),
                    ('MultivariateAnomalyDetection', '多指标异常检测算法'),
                ],
                db_index=True,
                max_length=64,
                verbose_name='算法类型',
            ),
        ),
    ]
