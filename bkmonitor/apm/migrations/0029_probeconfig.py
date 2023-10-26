# Generated by Django 3.2.15 on 2023-08-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apm", "0028_dbconfig"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProbeConfig",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("bk_biz_id", models.IntegerField(verbose_name="业务id")),
                ("app_name", models.CharField(max_length=128, verbose_name="应用名称")),
                ("config_level", models.CharField(max_length=50, verbose_name="配置级别")),
                ("config_key", models.CharField(max_length=255, verbose_name="配置key")),
                ("sn", models.CharField(max_length=255, verbose_name="配置变更标识")),
                ("rules", models.JSONField(verbose_name="配置")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
