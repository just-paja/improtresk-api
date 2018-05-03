"""Tests for reservation model."""

from dateutil.parser import parse
from django.test import TestCase

from model_mommy import mommy


class MealReservationTest(TestCase):
    """Test MealReservation methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        year = mommy.make('Year')
        meal_reservation = mommy.make(
            'MealReservation',
            food__name="Foo food",
            meal__date=parse("2016-12-23"),
            meal__name="lunch",
            meal__year=year,
            soup__name="Foo soup",
        )
        self.assertEqual(
            str(meal_reservation),
            'Reservation of Foo food and Foo soup for (%s) Lunch at Friday' % year.year,
        )
