"""Tests for participant model."""

from dateutil.parser import parse

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from freezegun import freeze_time

from mock import patch

from model_mommy import mommy


class ParticipantTokenTest(TestCase):

    @freeze_time("2017-01-20T03:04:05Z")
    def test_is_valid_not_expired(self):
        token = mommy.make(
            'api.ParticipantToken',
            valid_until=parse('2017-01-20T03:04:04Z'),
        )
        self.assertEquals(token.is_valid(), True)

    @freeze_time("2017-01-20T03:04:05Z")
    def test_is_valid_expired_on_second(self):
        token = mommy.make(
            'api.ParticipantToken',
            valid_until=parse('2017-01-20T03:04:05Z'),
        )
        self.assertEquals(token.is_valid(), False)

    @freeze_time("2017-01-20T03:04:05Z")
    def test_is_valid_expired(self):
        token = mommy.make(
            'api.ParticipantToken',
            valid_until=parse('2017-01-20T03:04:06Z'),
        )
        self.assertEquals(token.is_valid(), False)

    @freeze_time("2017-01-20T03:04:05Z")
    def test_name_representation_valid(self):
        token = mommy.make(
            'api.ParticipantToken',
            participant__name='Martin',
            token_type='password-reset',
            valid_until=parse('2017-01-20T03:04:04Z'),
        )
        self.assertEquals(
            str(token),
            '%s: %s, (%s)' % (
                'Martin',
                _('Password reset'),
                '2017-01-20 03:04:04+00:00'
            ),
        )

    @freeze_time("2017-01-20T03:04:05Z")
    def test_name_representation_expired(self):
        token = mommy.make(
            'api.ParticipantToken',
            participant__name='Martin',
            token_type='password-reset',
            valid_until=parse('2017-01-20T03:04:06Z'),
        )
        self.assertEquals(
            str(token),
            '%s: %s, (%s)' % ('Martin', _('Password reset'), 'expired'),
        )

    @patch('uuid.uuid4')
    @freeze_time("2017-01-20T03:04:05Z")
    def test_save_generate_token(self, mock_uuid):
        mock_uuid.return_value = 'generated-token'
        token = mommy.make('api.ParticipantToken', token=None)

        self.assertEquals(token.valid_until, parse('2017-01-22T03:04:05Z'))
        self.assertEquals(token.token, 'generated-token')
