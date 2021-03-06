# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-28 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20170322_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=255, verbose_name='Token')),
                ('token_type', models.CharField(choices=[('password-reset', 'Password reset'), ('email-confirm', 'E-mail confirmation')], max_length=31, verbose_name='Token type')),
                ('valid_until', models.DateTimeField(verbose_name='Expiration date')),
                ('used', models.BooleanField(default=False, verbose_name='Was token already used?')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='api.Participant', verbose_name='Participant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
