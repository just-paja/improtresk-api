from django.db import migrations


def forwards(apps, schema_editor):
    WorkshopLocation = apps.get_model('api_textual', 'WorkshopLocation')
    WorkshopLocationDescription = apps.get_model('api_textual', 'WorkshopLocationDescription')
    db_alias = schema_editor.connection.alias
    performers = WorkshopLocation.objects.using(db_alias).all()
    create = []

    for performer in performers:
        desc = performer.descriptions.filter(lang='cs').first()

        if not desc:
            desc = WorkshopLocationDescription(
                performer=performer,
                text=performer.text,
            )
            create.append(desc)

        performer.text = ''
        performer.save()
    WorkshopLocationDescription.objects.using(db_alias).bulk_create(create)


def backwards(apps, schema_editor):
    WorkshopLocationDescription = apps.get_model('api_textual', 'WorkshopLocationDescription')
    db_alias = schema_editor.connection.alias
    descriptions = WorkshopLocationDescription.objects.using(db_alias)\
        .filter(lang='cs')\
        .all()

    for desc in descriptions:
        performer = desc.performer
        if performer.text != desc.text:
            performer.text = desc.text
            performer.save()
        desc.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api_textual', '0018_workshoplocationdescription'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards,
        ),
    ]
