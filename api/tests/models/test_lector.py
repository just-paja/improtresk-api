"""Tests for workshop model."""
from api.models.lector import Lector

from django.test import TestCase


class LectorTest(TestCase):
    """Test lector methods."""

    def test_string_representation(self):
        """Test that lector turns to string properly."""
        entry = Lector(name="Foo Lector")
        self.assertEqual(str(entry), 'Foo Lector')
