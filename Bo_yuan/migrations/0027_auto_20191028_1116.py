# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-10-28 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bo_yuan', '0026_auto_20191028_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cars',
            name='ratio',
        ),
        migrations.AddField(
            model_name='cars',
            name='img6',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='cars',
            name='img7',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='cars',
            name='img8',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='cars',
            name='img9',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='cars',
            name='video',
            field=models.CharField(max_length=256, null=True),
        ),
    ]