"""Tests for reservation model."""
from api.models import Rules, Year

from django.test import TestCase


class YearTest(TestCase):
    """Test year methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        rules = Rules(text="foo", createdAt="2017-01-20T03:04:05")
        self.assertEqual(str(rules), 'Rules (2017-01-20T03:04:05)')
