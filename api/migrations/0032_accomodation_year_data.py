from django.db import migrations


def forwards(apps, schema_editor):
    Accomodation = apps.get_model('api', 'Accomodation')
    Year = apps.get_model('api', 'Year')
    db_alias = schema_editor.connection.alias

    year2017 = Year.objects.using(db_alias).get(year='2017')
    year2018 = Year.objects.using(db_alias).get(year='2018')
    accomodations = Accomodation.objects.using(db_alias).filter(year__isnull=True).all()

    for accomodation in accomodations:
        accomodation.year = year2017
        accomodation.save()
        descriptions = accomodation.descriptions.all()
        accomodation.pk = None
        accomodation.year = year2018
        accomodation.save()
        for description in descriptions:
            description.pk = None
            description.accomodation = accomodation
            description.save()


def backwards(apps, schema_editor):
    Accomodation = apps.get_model('api', 'Accomodation')
    Year = apps.get_model('api', 'Year')
    db_alias = schema_editor.connection.alias

    year2017 = Year.objects.using(db_alias).get(year='2017')
    year2018 = Year.objects.using(db_alias).get(year='2018')
    accomodations2017 = Accomodation.objects.using(db_alias).filter(year=year2017).all()
    accomodations2018 = Accomodation.objects.using(db_alias).filter(year=year2018).all()

    for accomodation in accomodations2018:
        accomodation.delete()

    for accomodation in accomodations2017:
        accomodation.year = None
        accomodation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_accomodation_year'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards,
        ),
    ]
