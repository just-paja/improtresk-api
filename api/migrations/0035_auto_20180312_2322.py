# Generated by Django 2.0.2 on 2018-03-12 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20180312_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='workshop_price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.WorkshopPrice', verbose_name='Workshop price'),
        ),
    ]
