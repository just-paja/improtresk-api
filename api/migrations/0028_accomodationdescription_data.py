from django.db import migrations


def forwards(apps, schema_editor):
    Accomodation = apps.get_model('api', 'Accomodation')
    AccomodationDescription = apps.get_model('api', 'AccomodationDescription')
    db_alias = schema_editor.connection.alias
    accomodations = Accomodation.objects.using(db_alias).all()
    create = []

    for accomodation in accomodations:
        desc = accomodation.descriptions.filter(lang='cs').first()

        if not desc:
            desc = AccomodationDescription(
                accomodation=accomodation,
                text=accomodation.desc,
            )
            create.append(desc)

        accomodation.text = ''
        accomodation.save()
    AccomodationDescription.objects.using(db_alias).bulk_create(create)


def backwards(apps, schema_editor):
    AccomodationDescription = apps.get_model('api', 'AccomodationDescription')
    db_alias = schema_editor.connection.alias
    descriptions = AccomodationDescription.objects.using(db_alias)\
        .filter(lang='cs')\
        .all()

    for desc in descriptions:
        accomodation = desc.accomodation
        if accomodation.desc != desc.text:
            accomodation.desc = desc.text
            accomodation.save()
        desc.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_accomodationdescription'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards,
        ),
    ]
