# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170209_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='api.Year', verbose_name='Year'),
        ),
    ]
