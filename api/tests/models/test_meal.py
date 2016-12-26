"""Tests for meal model."""
from django.test import TestCase
from api.models import Meal


class MealTest(TestCase):
    """Test Meal methods."""

    def test_string_representation(self):
        """Test that meal turns to string properly."""
        entry = Meal(name="Foo Meal")
        self.assertEqual(str(entry), 'Foo Meal')
