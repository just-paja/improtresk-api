"""Tests for PriceLevel model."""
from api.models.priceLevel import PriceLevel

from django.test import TestCase


class PriceLevelTest(TestCase):
    """Test PriceLevel methods."""

    def test_string_representation(self):
        """Test that PriceLevel turns to string properly."""
        entry = PriceLevel(name="Foo PriceLevel")
        self.assertEqual(str(entry), 'Foo PriceLevel')
