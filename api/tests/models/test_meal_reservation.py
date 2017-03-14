"""Tests for reservation model."""
from django.test import TestCase

from model_mommy import mommy


class MealReservationTest(TestCase):
    """Test MealReservation methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        meal_reservation = mommy.make(
            'MealReservation',
            food__name="Foo food",
            soup__name="Foo soup",
            meal__name="lunch",
            meal__date="2016-12-23"
        )
        self.assertEqual(
            str(meal_reservation),
            'Reservation of Foo food and Foo soup for lunch at 2016-12-23',
        )
