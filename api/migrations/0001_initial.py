# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-03 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('name', models.CharField(max_length=127)),
                ('desc', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('capacity', models.PositiveIntegerField(default=12)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccomodationPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('accomodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Accomodation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('name', models.CharField(max_length=127)),
                ('course', models.PositiveIntegerField(choices=[(1, 'Soup'), (2, 'Main course')])),
                ('price', models.PositiveIntegerField()),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('date', models.DateField()),
                ('capacity', models.PositiveIntegerField(default=12)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Food')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('name', models.CharField(max_length=127)),
                ('about', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LectorPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('lector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Lector')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('symvar', models.CharField(blank=True, max_length=63)),
                ('price', models.PositiveIntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('overPaid', models.BooleanField(default=False)),
                ('accomodation', models.ManyToManyField(to='api.Accomodation')),
                ('food', models.ManyToManyField(to='api.Food')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('team', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('birthday', models.CharField(max_length=255)),
                ('rules', models.BooleanField(default=False)),
                ('newsletter', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('ident', models.CharField(blank=True, max_length=255, unique=True)),
                ('symvar', models.CharField(blank=True, max_length=255)),
                ('symcon', models.CharField(blank=True, max_length=255)),
                ('symspc', models.CharField(blank=True, max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('sender', models.CharField(blank=True, max_length=255)),
                ('bank', models.CharField(blank=True, max_length=255)),
                ('currency', models.CharField(blank=True, max_length=255)),
                ('received', models.DateTimeField(blank=True, null=True)),
                ('message', models.TextField(blank=True, max_length=255)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('name', models.CharField(max_length=127)),
                ('desc', models.TextField()),
                ('difficulty', models.CharField(max_length=127)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('capacity', models.PositiveIntegerField(default=12)),
                ('lector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshops', to='api.Lector')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkshopPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('image', models.ImageField(upload_to='var/photos')),
                ('desc', models.CharField(max_length=255)),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Deleted')])),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Workshop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='participant',
            name='assignedWorkshop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Workshop'),
        ),
        migrations.AddField(
            model_name='order',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.Participant'),
        ),
        migrations.AddField(
            model_name='order',
            name='workshops',
            field=models.ManyToManyField(to='api.Workshop'),
        ),
    ]
