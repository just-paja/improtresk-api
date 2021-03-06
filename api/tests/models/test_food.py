"""Tests for Food model."""

from dateutil.parser import parse
from django.test import TestCase
from freezegun import freeze_time
from model_mommy import mommy


class FoodTest(TestCase):
    """Test Food methods."""

    def test_string_representation(self):
        """Test that Food turns to string properly."""
        year = mommy.make('Year')
        meal = mommy.make('Meal', date=parse("2017-02-01"), year=year)
        entry = mommy.make(
            'Food',
            name="Foo Food",
            meal=meal,
            capacity=20,
        )
        self.assertEqual(str(entry), '(%s, Wednesday) Foo Food (0/20)' % year.year)

    @freeze_time("2017-02-01")
    def test_capacity(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at='2017-03-01T00:00:00Z',
            food__capacity=1,
            reservation__order__paid=True,
        )
        meal_reservation.reservation.order.paid = True
        meal_reservation.reservation.order.save()
        food = meal_reservation.food
        self.assertEqual(food.number_of_reservations(), 1)
        self.assertEqual(food.has_free_capacity(), False)

    @freeze_time("2017-02-01")
    def test_capacity_after_reservation(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at='2017-01-01T00:00:00Z',
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
            reservation__ends_at='2017-01-01T00:00:00Z',
            food__capacity=1,
            reservation__order__paid=True,
            reservation__order__participant__name="Foo participant",
        )
        meal_reservation.reservation.order.paid = True
        meal_reservation.reservation.order.save()
        food = meal_reservation.food
        self.assertEqual(food.number_of_reservations(), 1)
        self.assertEqual(food.has_free_capacity(), False)
