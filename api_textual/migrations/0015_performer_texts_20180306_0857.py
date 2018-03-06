from django.db import migrations

def forwards(apps, schema_editor):
    Performer = apps.get_model('api_textual', 'Performer')
    PerformerDescription = apps.get_model('api_textual', 'PerformerDescription')
    db_alias = schema_editor.connection.alias
    performers = Performer.objects.using(db_alias).all()
    create = []

    for performer in performers:
        desc = performer.descriptions.filter(lang='cs').first()

        if not desc:
            desc = PerformerDescription(
                performer=performer,
                text=performer.text,
            )
            create.push(desc)

        performer.text = ''
        performer.save()
    PerformerDescription.objects.using(db_alias).bulk_create(create)

def backwards(apps, schema_editor):
    PerformerDescription = apps.get_model('api_textual', 'PerformerDescription')
    db_alias = schema_editor.connection.alias
    descriptions = PerformerDescription.objects.using(db_alias)\
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
        ('api_textual', '0014_auto_20180306_0757'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards,
        ),
    ]
