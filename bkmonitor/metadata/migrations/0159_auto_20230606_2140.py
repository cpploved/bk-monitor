# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2023-06-06 13:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0158_merge_20230602_1155'),
    ]

    operations = [migrations.RunSQL('ALTER table metadata_space AUTO_INCREMENT=2;')]
