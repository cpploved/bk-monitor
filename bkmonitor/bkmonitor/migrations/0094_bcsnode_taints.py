# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2022-04-24 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bkmonitor", "0093_merge_20220424_1452"),
    ]

    operations = [
        migrations.AddField(
            model_name="bcsnode",
            name="taints",
            field=models.TextField(null=True),
        ),
    ]
