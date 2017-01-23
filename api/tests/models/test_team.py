"""Tests for team model."""
from api.models.team import Team

from django.test import TestCase


class TeamTest(TestCase):
    """Test Team methods."""

    def test_string_representation(self):
        """Test that team turns to string properly."""
        entry = Team(name="Foo team")
        self.assertEqual(str(entry), 'Foo team')
