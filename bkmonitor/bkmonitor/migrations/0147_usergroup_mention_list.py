# Generated by Django 3.2.15 on 2023-10-16 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkmonitor', '0146_merge_20231010_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='mention_list',
            field=models.JSONField(default=list, verbose_name='告警提醒人'),
        ),
    ]
