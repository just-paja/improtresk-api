# Generated by Django 2.0.2 on 2018-03-06 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_participant_workshops_20180131_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccomodationDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('lang', models.CharField(choices=[('cs', 'Česky'), ('en', 'English')], default='cs', max_length=16, verbose_name='Language')),
                ('accomodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descriptions', to='api.Accomodation', verbose_name='Accomodation')),
            ],
            options={
                'verbose_name': 'Text slug',
                'verbose_name_plural': 'Text slugs',
                'abstract': False,
            },
        ),
    ]