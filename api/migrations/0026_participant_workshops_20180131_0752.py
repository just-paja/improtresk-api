from django.db import migrations

def forwards(apps, schema_editor):
    Participant = apps.get_model('api', 'Participant')
    ParticipantWorkshop = apps.get_model('api', 'ParticipantWorkshop')
    db_alias = schema_editor.connection.alias
    participants = Participant.objects.using(db_alias).filter(assigned_workshop__isnull=False).all()

    for participant in participants:
        ws = ParticipantWorkshop.objects.using(db_alias).filter(
            participant=participant,
            workshop=participant.assigned_workshop,
        ).first()

        if not ws:
            ws = ParticipantWorkshop(
                participant=participant,
                workshop=participant.assigned_workshop,
            )
            ws.ignore_change = True
            ParticipantWorkshop.objects.using(db_alias).bulk_create([ws])

        participant.assigned_workshop = None
        participant.save()

def backwards(apps, schema_editor):
    ParticipantWorkshop = apps.get_model('api', 'ParticipantWorkshop')
    db_alias = schema_editor.connection.alias
    workshops = ParticipantWorkshop.objects.using(db_alias).all()

    for workshop in workshops:
        participant = workshop.participant
        if participant.assigned_workshop != workshop:
            participant.ignore_change = True
            participant.assigned_workshop = workshop
            participant.save()
        workshop.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_participantworkshop'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards,
        ),
    ]
