"""Tests for PriceLevel model."""
from django.test import TestCase

from model_mommy import mommy


class PriceLevelTest(TestCase):
    """Test PriceLevel methods."""

    def test_string_representation(self):
        """Test that PriceLevel turns to string properly."""
        entry = mommy.make(
            'PriceLevel',
            name="Foo PriceLevel",
            year__year="1234",
        )
        self.assertEqual(str(entry), 'Foo PriceLevel (1234)')
