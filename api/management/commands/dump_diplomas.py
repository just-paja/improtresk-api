#!/usr/bin/env python
import json

from django.core.management.base import BaseCommand

from ...models import Year, Workshop


class Command(BaseCommand):
    help = 'Parses FIO bank statements'

    def handle(self, *args, **kwargs):
        year = Year.objects.get_current()
        data = {}
        for workshop in Workshop.objects.filter(year=year).all():
            data[workshop.id] = []
            for participant in workshop.participants.all():
                data[workshop.id].append({
                    'participant_name': participant.participant.name,
                    'workshop_name': workshop.name,
                    'lector_name': ', '.join([
                        lector.name for lector in workshop.lectors.all()
                    ]),
                })
        with open('improtresk-diploma-data.json', 'w') as outfile:
            json.dump(data, outfile)
