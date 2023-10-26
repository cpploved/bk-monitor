# Generated by Django 3.2.15 on 2023-08-03 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_databus', '0036_auto_20230719_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='datalinkconfig',
            name='is_edge_transport',
            field=models.BooleanField(default=False, verbose_name='是否为边缘存查链路'),
        ),
        migrations.AlterField(
            model_name='datalinkconfig',
            name='deploy_options',
            field=models.JSONField(blank=True, default=dict, verbose_name='采集下发选项'),
        ),
    ]
