"""Tests for reservation model."""
from django.test import TestCase

from model_mommy import mommy


class ReservationTest(TestCase):
    """Test workshop methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        workshop = mommy.make('api.Workshop', name="Foo workshop")
        price_level = mommy.make('api.PriceLevel', name="Foo price level")
        workshop_price = mommy.make(
            'api.WorkshopPrice',
            price=123,
            workshop=workshop,
            price_level=price_level,
        )
        entry = mommy.make(
            'api.Reservation',
            workshop_price=workshop_price,
            ends_at="2017-01-01",
        )
        self.assertEqual(str(entry), 'Foo workshop for 123 ends at 2017-01-01')
