# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-10-24 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bo_yuan', '0017_appointments_car_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='car_user',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='users',
            name='openid',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='wx_name',
            field=models.CharField(max_length=256),
        ),
    ]
