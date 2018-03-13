"""Tests for participant model."""

from django.core import mail
from django.test import TestCase

from mock import patch

from model_mommy import mommy


class ParticipantTest(TestCase):
    def setUp(self):
        self.maxDiff = 100000
        mail.outbox = []
        self.participant = mommy.make(
            'api.Participant',
            name="Foo participant",
            email="foo@bar.com",
        )
        self.participant.request_password_reset()

    @patch('uuid.uuid4')
    def test_mail_update_sent_to_participant(self, mock_uuid4):
        mock_uuid4.return_value = 'generated-token'
        self.participant.request_password_reset()
        self.assertEquals(mail.outbox.pop().to, ['foo@bar.com'])

    @patch('uuid.uuid4')
    def test_mail_update_contains_url(self, mock_uuid4):
        mock_uuid4.return_value = 'generated-token'
        self.participant.request_password_reset()
        self.assertIn('/cs/nove-heslo?token=generated-token', mail.outbox.pop().body)
