"""Tests for workshop model."""
from django.test import TestCase
from api.models.lector import Lector


class LectorTest(TestCase):
    """Test lector methods."""

    def test_string_representation(self):
        """Test that lector turns to string properly."""
        entry = Lector(name="Foo Lector")
        self.assertEqual(str(entry), 'Foo Lector')
