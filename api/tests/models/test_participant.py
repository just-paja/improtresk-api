"""Tests for participant model."""

from django.core import mail
from django.test import TestCase

from mock import patch

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
            'Prev workshop: Foo workshop, '
            'Current workshop: Foo workshop, '
            'Workshop preferences foo\n'
            'Organizační tým Improtřesku\n'
            'http://improtresk.cz\n'
            'info@improtresk.cz\n'
            '\n'
            '--\n'
            '\n'
            'Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.\n',
        )

    @patch('uuid.uuid4')
    def test_request_password_reset(self, mock_uuid4):
        self.maxDiff = 100000
        mail.outbox = []
        mock_uuid4.return_value = 'generated-token'
        participant = mommy.make(
            'api.Participant',
            name="Foo participant",
            email="foo@bar.com",
        )
        participant.request_password_reset()
        self.assertEquals(len(mail.outbox), 1)
        sent = mail.outbox.pop()
        self.assertEquals(sent.to, ['foo@bar.com'])
        self.assertEquals(
            sent.body,
            """Ahoj,

dostali jsme žádost na obnovu hesla k tvému účtu na Improtřesk. Pro zadání \
nového hesla následuj následující odkaz:

http://improtresk.cz/nove-heslo?token=generated-token

    -----

Pokud jsi o změnu hesla nepožádal, tak tento e-mail ignoruj.

Organizační tým Improtřesku
http://improtresk.cz
info@improtresk.cz

--

Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.
""",
        )
