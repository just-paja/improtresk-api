"""Tests for workshop model."""
from api.models import PriceLevel, Workshop, WorkshopPrice

from django.test import TestCase


class WorkshopPriceTest(TestCase):
    """Test WorkshopPrice methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        workshop = Workshop(name="Foo workshop")
        price_level = PriceLevel(name="Foo price level")
        entry = WorkshopPrice(price=123, workshop=workshop, price_level=price_level)
        self.assertEqual(str(entry), 'Foo workshop - Foo price level (123,-)')
