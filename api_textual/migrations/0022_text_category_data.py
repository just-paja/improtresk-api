from django.db import migrations

conversion_table = {
    'about-festival-short': 'homepage',
    'accomodation-intro': 'accomodation',
    'food-intro': 'food',
    'what-do-you-pay-for': 'fees',
    'how-to-pay': 'fees',
    'how-to-sign-out': 'fees',
    'locations-intro': 'locations',
    'schedule-intro': 'schedule',
}


def forwards(apps, schema_editor):
    Text = apps.get_model('api_textual', 'Text')
    db_alias = schema_editor.connection.alias
    texts = Text.objects.using(db_alias).all()

    for text in texts:
        if text.slug in conversion_table:
            text.category = conversion_table[text.slug]
            text.save()


def backwards(apps, schema_editor):
    Text = apps.get_model('api_textual', 'Text')
    db_alias = schema_editor.connection.alias
    texts = Text.objects.using(db_alias).all()

    for text in texts:
        text.category = None
        text.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api_textual', '0021_text_category'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards,
        ),
    ]
