# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_status_tests_skip'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstatus',
            name='tests_fail',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectstatus',
            name='tests_pass',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectstatus',
            name='tests_skip',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectstatus',
            name='metrics_summary',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
