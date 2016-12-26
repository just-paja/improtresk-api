"""Tests for Food model."""
from django.test import TestCase
from api.models import Food


class FoodTest(TestCase):
    """Test Food methods."""

    def test_string_representation(self):
        """Test that Food turns to string properly."""
        entry = Food(name="Foo Food")
        self.assertEqual(str(entry), 'Foo Food')
