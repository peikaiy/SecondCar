# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-10-24 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bo_yuan', '0020_auto_20191024_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='brands',
            name='weight',
            field=models.IntegerField(default=1),
        ),
    ]
