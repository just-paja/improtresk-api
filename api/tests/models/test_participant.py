"""Tests for participant model."""
from django.test import TestCase

from model_mommy import mommy


class ParticipantTest(TestCase):

    def test_getReassignmentMailBody(self):
        participant = mommy.make(
            'api.Participant',
            name="Foo participant",
            assigned_workshop__name="Foo workshop",
            assigned_workshop__lectors={
                mommy.make(
                    'api.Lector',
                    name="Foo lector",
                ),
            },
        )
        template = (
            'Prev workshop: {prevWorkshop}, '
            'Current workshop: {currentWorkshop}, '
            'Workshop preferences {workshopPreferences}'
        )

        self.assertEquals(
            participant.getReassignmentMailBody(template),
            'Prev workshop: Foo lector: Foo workshop, '
            'Current workshop: Foo lector: Foo workshop, '
            'Workshop preferences foo\n'
            'Organizační tým Improtřesku 2017\n'
            'http://improtresk.cz\n'
            'info@improtresk.cz\n'
            '\n'
            '--\n'
            '\n'
            'Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.\n',
        )
