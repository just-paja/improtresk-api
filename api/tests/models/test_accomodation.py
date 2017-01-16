"""Tests for workshop model."""
import datetime

from api.models.accomodation import Accomodation

from django.test import TestCase

from freezegun import freeze_time

from model_mommy import mommy


class AccomodationTest(TestCase):
    """Test accomodation methods."""

    def test_string_representation(self):
        """Test that accomodation turns to string properly."""
        entry = Accomodation(name="Foo Accomodation")
        self.assertEqual(str(entry), 'Foo Accomodation')

    @freeze_time("2017-2-1")
    def test_capacity(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=datetime.datetime(year=2017, month=3, day=1),
            accomodation__capacity=1,
            order__paid=False,
        )
        accomodation = reservation.accomodation
        self.assertEqual(accomodation.number_of_reservations(), 1)
        self.assertEqual(accomodation.has_free_capacity(), False)

    @freeze_time("2017-2-1")
    def test_capacity_after_reservation(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=datetime.datetime(year=2017, month=1, day=1),
            accomodation__capacity=1,
            order__paid=False,
        )
        accomodation = reservation.accomodation
        self.assertEqual(accomodation.number_of_reservations(), 0)
        self.assertEqual(accomodation.has_free_capacity(), True)

    @freeze_time("2017-2-1")
    def test_capacity_paid(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=datetime.datetime(year=2017, month=1, day=1),
            accomodation__capacity=1,
            order__paid=True,
        )
        accomodation = reservation.accomodation
        self.assertEqual(accomodation.number_of_reservations(), 1)
        self.assertEqual(accomodation.has_free_capacity(), False)
