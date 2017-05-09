"""Tests for reservation model."""
from django.test import TestCase

from model_mommy import mommy


class FestivalTest(TestCase):
    """Test year methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        year = mommy.make(
            'Festival',
            name="Improtřesk",
        )
        self.assertEqual(str(year), 'Festival Improtřesk')
