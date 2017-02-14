"""Tests for participant backend."""

from api.auth.participant_backend import ParticipantBackend

from django.test import TestCase

from model_mommy import mommy


class ParticipantBackendTest(TestCase):
    """Test accomodation methods."""

    def setUp(self):
        self.backend = ParticipantBackend()

    def test_get_user_exists(self):
        """Test that user is returned if user ID exists."""
        user_expected = mommy.make('api.Participant', id=1)
        user_returned = self.backend.get_user(1)
        self.assertEqual(user_returned, user_expected)

    def test_get_user_missing(self):
        """Test that method returns None if user ID does not exists."""
        self.assertEqual(self.backend.get_user(1), None)

    def test_authenticate_email_does_not_exist(self):
        """Test that authenticate returns None when user email does not exist."""
        self.assertEqual(self.backend.authenticate('user@localhost'), None)

    def test_authenticate_password_does_not_match(self):
        """Test that authenticate returns None when user password does not match."""
        mommy.make(
            'api.Participant',
            id=1,
            email='user@localhost',
            password='test'
        )
        user_returned = self.backend.authenticate('user@localhost', 'badPassword')
        self.assertEqual(user_returned, None)

    def test_authenticate_success(self):
        """Test that authenticate is successful when passwords match."""
        user_expected = mommy.make(
            'api.Participant',
            id=1,
            email='user@localhost',
            password='pbkdf2_sha256$30000$X7Z52JrOXt7N$DJ/wi15DOP+zi9yI/aJQIXKQEBovydyyTJ3v3zORmT0='
        )
        user_returned = self.backend.authenticate('user@localhost', '3CX3Fe5hNI')
        self.assertEqual(user_returned, user_expected)
