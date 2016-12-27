"""Tests for workshop model."""
from django.test import TestCase
from api.models.workshop import WorkshopDifficulty


class WorkshopDifficultyTest(TestCase):
    """Test WorkshopDifficulty methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        entry = WorkshopDifficulty(name="Foo WorkshopDifficulty")
        self.assertEqual(str(entry), 'Foo WorkshopDifficulty')
