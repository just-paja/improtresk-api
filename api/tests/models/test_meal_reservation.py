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
            meal__name="lunch",
        )
        self.assertEqual(str(meal_reservation), 'Reservation of Foo food for lunch')
