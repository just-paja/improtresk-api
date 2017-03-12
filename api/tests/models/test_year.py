"""Tests for reservation model."""
from django.test import TestCase

from model_mommy import mommy


class YearTest(TestCase):
    """Test year methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        year = mommy.make(
            'Year',
            year="1234",
        )
        self.assertEqual(str(year), 'Year 1234')

    def test_get_actual_price_level_none(self):
        year = mommy.make('Year')
        self.assertEqual(year.get_actual_price_level(), None)

    def test_get_actual_price_level(self):
        price_level = mommy.make('PriceLevel')
        year = mommy.make(
            'Year',
            price_levels=[price_level],
        )
        self.assertEqual(year.get_actual_price_level(), price_level)
