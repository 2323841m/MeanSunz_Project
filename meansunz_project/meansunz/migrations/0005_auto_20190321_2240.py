# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-21 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meansunz', '0004_auto_20190321_2231'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='rating',
            new_name='rating_post',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rating_comment',
            field=models.IntegerField(default=0),
        ),
    ]
