# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-09 22:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170130_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomodationphoto',
            name='height',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='accomodationphoto',
            name='width',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='foodphoto',
            name='height',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='foodphoto',
            name='width',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='lectorphoto',
            name='height',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='lectorphoto',
            name='width',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='workshopphoto',
            name='height',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='workshopphoto',
            name='width',
            field=models.PositiveIntegerField(blank=True, default=100, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='accomodationphoto',
            name='image',
            field=models.ImageField(height_field='height', upload_to='var/photos', width_field='width'),
        ),
        migrations.AlterField(
            model_name='foodphoto',
            name='image',
            field=models.ImageField(height_field='height', upload_to='var/photos', width_field='width'),
        ),
        migrations.AlterField(
            model_name='lectorphoto',
            name='image',
            field=models.ImageField(height_field='height', upload_to='var/photos', width_field='width'),
        ),
        migrations.AlterField(
            model_name='pricelevel',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_levels', to='api.Year', verbose_name='Year'),
        ),
        migrations.AlterField(
            model_name='workshopphoto',
            name='image',
            field=models.ImageField(height_field='height', upload_to='var/photos', width_field='width'),
        ),
        migrations.AlterField(
            model_name='workshopprice',
            name='price_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshop_prices', to='api.PriceLevel', verbose_name='Price level'),
        ),
        migrations.AlterField(
            model_name='workshopprice',
            name='workshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='api.Workshop', verbose_name='Workshop'),
        ),
    ]
