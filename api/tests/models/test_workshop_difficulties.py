"""Tests for workshop model."""
from api.models.workshop import WorkshopDifficulty

from django.test import TestCase


class WorkshopDifficultyTest(TestCase):
    """Test WorkshopDifficulty methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        entry = WorkshopDifficulty(name="Foo WorkshopDifficulty")
        self.assertEqual(str(entry), 'Foo WorkshopDifficulty')
