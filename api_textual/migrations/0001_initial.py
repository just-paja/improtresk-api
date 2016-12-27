# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Identifier')),
                ('text', models.TextField(verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Text items',
                'verbose_name': 'Text item',
            },
        ),
        migrations.CreateModel(
            name='TextPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api_textual.Text', verbose_name='Text')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
