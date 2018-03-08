from django.db import migrations


def forwards(apps, schema_editor):
    Order = apps.get_model('api', 'Order')
    Year = apps.get_model('api', 'Year')
    db_alias = schema_editor.connection.alias

    year = Year.objects.using(db_alias).get(year='2017')
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
