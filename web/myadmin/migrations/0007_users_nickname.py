# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-04 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0006_auto_20180703_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='nickname',
            field=models.CharField(max_length=20, null=True),
        ),
    ]