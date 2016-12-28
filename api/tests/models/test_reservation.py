"""Tests for reservation model."""
from api.models import PriceLevel, Reservation, Workshop, WorkshopPrice

from django.test import TestCase


class ReservationTest(TestCase):
    """Test workshop methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        workshop = Workshop(name="Foo workshop")
        price_level = PriceLevel(name="Foo price level")
        workshop_price = WorkshopPrice(price=123, workshop=workshop, price_level=price_level)
        entry = Reservation(workshop_price=workshop_price, ends_at="2017-1-1")
        self.assertEqual(str(entry), 'Foo workshop for 123 ends at 2017-1-1')
