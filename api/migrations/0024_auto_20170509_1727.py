# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-09 17:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_year_end_food_picking_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Festival name')),
                ('discontinued', models.BooleanField(default=False, help_text='Was festival discontinued', verbose_name='Discontinued')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='year',
            name='festival',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='api.Festival', verbose_name='Festival'),
        ),
    ]
