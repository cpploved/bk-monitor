# Generated by Django 3.2.15 on 2023-09-07 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkmonitor', '0142_auto_20230821_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='metric_type',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='指标类型'),
        ),
    ]
