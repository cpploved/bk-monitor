# Generated by Django 3.2.15 on 2023-08-03 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0165_spacevminfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusterinfo',
            name='ssl_certificate',
            field=models.TextField(default='', null=True, verbose_name='SSL/TLS 证书内容'),
        ),
        migrations.AddField(
            model_name='clusterinfo',
            name='ssl_certificate_authorities',
            field=models.TextField(default='', null=True, verbose_name='CA 内容'),
        ),
        migrations.AddField(
            model_name='clusterinfo',
            name='ssl_certificate_key',
            field=models.TextField(default='', null=True, verbose_name='SSL/TLS 证书私钥内容'),
        ),
        migrations.AddField(
            model_name='clusterinfo',
            name='ssl_insecure_skip_verify',
            field=models.BooleanField(default=False, verbose_name='是否跳过服务器校验'),
        ),
        migrations.AddField(
            model_name='clusterinfo',
            name='ssl_verification_mode',
            field=models.CharField(default='none', max_length=16, null=True, verbose_name='CA 校验模式'),
        ),
    ]
