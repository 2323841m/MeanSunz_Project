# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-21 00:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meansunz', '0012_auto_20190321_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meansunz.UserProfile'),
        ),
    ]
