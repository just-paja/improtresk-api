"""Tests for meal model."""
import datetime

from api.models import Meal

from django.test import TestCase

from freezegun import freeze_time

from model_mommy import mommy


class MealTest(TestCase):
    """Test Meal methods."""

    def test_string_representation(self):
        """Test that meal turns to string properly."""
        entry = Meal(
            name="Foo Meal",
            course=1,
            date="2017-02-01",
        )
        self.assertEqual(str(entry), 'Foo Meal Soup at 2017-02-01')

    @freeze_time("2017-02-01")
    def test_capacity(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at=datetime.datetime(year=2017, month=3, day=1),
            meal__capacity=1,
            reservation__order__paid=False,
        )
        meal = meal_reservation.meal
        self.assertEqual(meal.number_of_reservations(), 1)
        self.assertEqual(meal.has_free_capacity(), False)

    @freeze_time("2017-02-01")
    def test_capacity_after_reservation(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at=datetime.datetime(year=2017, month=1, day=1),
            meal__capacity=1,
            reservation__order__paid=False,
        )
        meal = meal_reservation.meal
        self.assertEqual(meal.number_of_reservations(), 0)
        self.assertEqual(meal.has_free_capacity(), True)

    @freeze_time("2017-02-01")
    def test_capacity_paid(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at=datetime.datetime(year=2017, month=1, day=1),
            meal__capacity=1,
            reservation__order__paid=True,
        )
        meal = meal_reservation.meal
        self.assertEqual(meal.number_of_reservations(), 1)
        self.assertEqual(meal.has_free_capacity(), False)
