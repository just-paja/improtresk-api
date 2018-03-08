from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


def forwards(apps, schema_editor):
    Order = apps.get_model('api', 'Order')
    Year = apps.get_model('api', 'Year')
    db_alias = schema_editor.connection.alias

    try:
        year = Year.objects.using(db_alias).get(year='2017')
    except ObjectDoesNotExist:
        year = None

    if year:
        orders = Order.objects.using(db_alias).filter(year__isnull=True).all()

        for order in orders:
            order.year = year
            order.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_order_year'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards,
        ),
    ]
