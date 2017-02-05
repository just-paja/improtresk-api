"""Tests for reservation model."""
from django.test import TestCase

from model_mommy import mommy


class YearTest(TestCase):
    """Test year methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        year = mommy.make(
            'Year',
            year="1234",
        )
        self.assertEqual(str(year), 'Year 1234')
