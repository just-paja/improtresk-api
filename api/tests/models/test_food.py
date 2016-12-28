"""Tests for Food model."""
import datetime

from api.models import Food

from django.test import TestCase

from freezegun import freeze_time

from model_mommy import mommy


class FoodTest(TestCase):
    """Test Food methods."""

    def test_string_representation(self):
        """Test that Food turns to string properly."""
        entry = Food(name="Foo Food")
        self.assertEqual(str(entry), 'Foo Food')

    @freeze_time("2017-02-01")
    def test_capacity(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at=datetime.datetime(year=2017, month=3, day=1),
            food__capacity=1,
            reservation__order__paid=False,
        )
        food = meal_reservation.food
        self.assertEqual(food.number_of_reservations(), 1)
        self.assertEqual(food.has_free_capacity(), False)

    @freeze_time("2017-02-01")
    def test_capacity_after_reservation(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at=datetime.datetime(year=2017, month=1, day=1),
            food__capacity=1,
            reservation__order__paid=False,
        )
        food = meal_reservation.food
        self.assertEqual(food.number_of_reservations(), 0)
        self.assertEqual(food.has_free_capacity(), True)

    @freeze_time("2017-02-01")
    def test_capacity_paid(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at=datetime.datetime(year=2017, month=1, day=1),
            food__capacity=1,
            reservation__order__paid=True,
        )
        food = meal_reservation.food
        self.assertEqual(food.number_of_reservations(), 1)
        self.assertEqual(food.has_free_capacity(), False)
