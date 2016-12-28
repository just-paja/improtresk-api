"""Tests for PriceLevel model."""
from django.test import TestCase
from api.models.priceLevel import PriceLevel


class PriceLevelTest(TestCase):
    """Test PriceLevel methods."""

    def test_string_representation(self):
        """Test that PriceLevel turns to string properly."""
        entry = PriceLevel(name="Foo PriceLevel")
        self.assertEqual(str(entry), 'Foo PriceLevel')
